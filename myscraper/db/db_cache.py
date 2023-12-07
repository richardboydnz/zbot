from typing import Dict, Optional, Type, Callable
from scrapy import Item # type: ignore
from ..db import connection

from myscraper.db.db_store import DBMapping, KeyedDbStore, SimpleDbStore  # type: ignore
from ..items.item_cache import GeneratorCache, ItemCache

class DbCache(GeneratorCache):
    # enforces a unique keyed field
    def __init__(self, db: connection, map: DBMapping ):
        super().__init__(map.key_field)
        self.db_store = KeyedDbStore(db, map)
        self.id_field = map.id_field
        self.key_field = map.key_field
        # self.create_fetch_sql()

    # def create_fetch_sql(self):
    #     db_fields = list(self.db_storemap.item_to_db_map.keys())

    def generator(self, key: str) -> Optional[Item]:
        # item does not exist in cache - first try DB
        # item = self.db_store.fetch_item(key)
        # if not item is None:
        #     print('------- Retrieve from database', item)
        #     return item
        # return super().generate(key)
        return self.db_store.fetch_item(key)


    def store_item(self, item: Item):
        # do not store if exists
        # store in 2 layers of cache
        key = item[self.key_field]
        cached_item = self.fetch_item(key)
        if cached_item is not None:
            return cached_item
        
        db_item = self.db_store.store_item(item)
        super().store_item(db_item)
        return db_item

    def get_id(self, key: str) -> Optional[int]:
        item = self.gen_item(key)
        if item is None:
            return None
        
        return item.get(self.id_field, None)

    def fetch_item(self, key: str) -> Item:
        # fetch and store in 2 layers of cache
        cached_item = super().fetch_item(key)
        if cached_item is not None:
            return cached_item

        db_item = self.db_store.fetch_item(key)
        if db_item is not None:
            super().store_item(db_item)
        return db_item

    
class DbGeneratorCache(DbCache):
    def __init__(self, db: connection, map: DBMapping,
                 backup_fetch: Callable[[str], Optional[Item]]):
        super().__init__(db, map)
        self.__backup_fetch2 = backup_fetch

    def generate(self, key: str) -> Optional[Item]:
        # First, attempt to fetch the item using the existing database logic
        item = super().generate(key) # first look in the db
        if item is None:
            item = self.__backup_fetch2(key)
        return item
    

