from typing import Dict, Optional, Type
from scrapy import Item  # type: ignore
from ..items.item_cache import SingletonCache

class DbCache(SingletonCache):
    def __init__(self, cursor, key_field: str, id_field: str, db_table: str, field_mapping: Dict[str, str], itemClass: Type[Item] ):
        super().__init__(key_field, self._create_singleton)
        self.id_field = id_field
        self.db_table = db_table
        self.itemClass = itemClass
        self.field_mapping = field_mapping
        self.cursor = cursor
        self.create_fetch_sql()

    def create_fetch_sql(self):
        db_fields = list(self.field_mapping.keys())
        self.fetch_sql = f"SELECT {self.id_field}, {', '.join(db_fields)} FROM {self.db_table} WHERE {self.key_field} = %s"
        placeholders = ', '.join(['%s'] * len(db_fields))
        self.store_sql = f"INSERT INTO {self.db_table} ({', '.join(db_fields)}) VALUES ({placeholders}) RETURNING {self.id_field};"

    def _create_singleton(self, key: str) -> Optional[Item]:
        self.cursor.execute(self.fetch_sql, (key,))
        row = self.cursor.fetchone()
        if row:
            item_data = {item_field: row[i + 1] for i, item_field 
                         in enumerate(self.field_mapping.values())}
            item_data[self.id_field] = row[0]
            item = self.itemClass(**item_data)
            return item
        return None

    def store_item(self, item: Item) -> int:
        values = tuple(item[field] for field in self.field_mapping.values())
        self.cursor.execute(self.store_sql, values)
        new_item_id = self.cursor.fetchone()[0]
        item[self.id_field] = new_item_id
        super().store_item(item)
        return new_item_id

    def get_id(self, key: str) -> Optional[int]:
        item = self.fetch_item(key)
        return item.get(self.id_field) if item else None
