from typing import Dict, Optional, Type, Callable
from scrapy import Item # type: ignore
from ..db import connection

from myscraper.db.db_store import DBMapping, SimpleDbStore  # type: ignore
from ..items.item_cache import SingletonCache

class DbCache(SingletonCache):
    def __init__(self, db: connection, map: DBMapping ):
        super().__init__(map.key_field, self._backup_fetch)
        self.db_store = SimpleDbStore(db, map)
        self.id_field = map.id_field
        # self.create_fetch_sql()

    # def create_fetch_sql(self):
    #     db_fields = list(self.db_storemap.item_to_db_map.keys())

    def _backup_fetch(self, key: str) -> Optional[Item]:
        return self.db_store.fetch_item(key)

    def store_item(self, item: Item):
        db_item = self.db_store.store_item(item)
        super().store_item(db_item)
        return db_item

    def get_id(self, key: str) -> Optional[int]:
        item = self.fetch_item(key)
        return item.get(self.id_field) if item else None


class DBSingletonCache(DbCache):
    def __init__(self, db: connection, map: DBMapping,
                 backup_fetch: Callable[[str], Optional[Item]]):
        super().__init__(db, map)
        self.__backup_fetch_2 = backup_fetch

    def _backup_fetch(self, key: str) -> Optional[Item]:
        # First, attempt to fetch the item using the existing database logic
        item = super()._backup_fetch(key)

        # If the item is not found, use the provided generator function to create it
        if item is None:
            item = self.__backup_fetch_2(key)

        return item

