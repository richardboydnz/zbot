from typing import Any, Dict, NamedTuple, Type, Optional
from scrapy import Item  # type: ignore
from ..db import connection
from ..items import get_class

class DBMapping(NamedTuple):
    item_to_db: Dict[str, str]
    itemClass: Type[Item]
    db_table: str
    key_field: str
    id_field: str
    
class SimpleDbStore:
    # Does not check for uniqueness on key field
    # As there is no key, there is no need for a query
    # id field assigned by DB and returned in query
    def __init__(self, db: connection, map: DBMapping ):
        self.map = map
        self.db = db
        self.create_store_sql()

    def create_store_sql(self):
        self.db_fields = list(self.map.item_to_db.keys())
        placeholders = ', '.join(['%s'] * len(self.db_fields))
        self.store_sql = f"INSERT INTO {self.map.db_table} ({', '.join(self.db_fields)}) VALUES ({placeholders}) RETURNING {self.map.id_field};"

    def store_item(self, item: Item) -> Item:
        # stores and returns item with the correct id
        values = tuple(item[field] for field in self.map.item_to_db.values())
        with self.db.cursor() as cursor:
            # print('--- Store: ', get_class(item))
            cursor.execute(self.store_sql, values)
            new_item_id = cursor.fetchone()
            # print('--- result: ', get_class(item), new_item_id)

            if new_item_id:
                item[self.map.id_field] = new_item_id[0]
                return item
            raise ValueError("Failed to retrieve new item ID after insertion.")

class KeyedDbStore(SimpleDbStore):
    # checks on key value before storing
    # allows fetching on key value
    def create_store_sql(self):
        super().create_store_sql()
        self.fetch_sql = f"SELECT {self.map.id_field}, {', '.join(self.db_fields)} FROM {self.map.db_table} WHERE {self.map.key_field} = %s"

    def fetch_item(self, key:str) -> Item:
        with self.db.cursor() as cursor:
            # print('--- Fetch: ', key)
            cursor.execute(self.fetch_sql, (key,))
            row = cursor.fetchone()
            if row:
                item_data = {item_field: row[i + 1] for i, item_field 
                            in enumerate(self.map.item_to_db.values())}
                item_data[self.map.id_field] = row[0]
                item = self.map.itemClass(**item_data)
                return item
            return None
    
    def store_item(self, item: Item) -> Item:
        db_item = self.fetch_item(item[self.map.key_field])
        if db_item is None:
            db_item = super().store_item(item)
        return db_item


