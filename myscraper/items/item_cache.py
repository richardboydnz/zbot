from typing import Callable, Dict, Optional
from scrapy import Item  # type: ignore

class ItemCache:
    def __init__(self, key_field: str):
        self.cache: Dict[str, Item] = {}  # Cache to store Item objects
        self.key_field = key_field  # Key field for identifying items

    def fetch_item(self, key: str) -> Item:
        # Check if item is already in cache
        item = self.cache.get(key)
        return item

    def update_item(self, cachedItem: Item, newItem: Item):
        pass

    def store_item(self, item: Item) -> Item:
        key = item[self.key_field]
        cached_item = ItemCache.fetch_item(self,key)
        if cached_item is not None:
            self.update_item(cached_item, item)
        else:
            self.cache[key] = item
        return item

class GeneratorCache(ItemCache):
    def __init__(self, key_field: str, backup_fetch_func: Optional[Callable[[str], Optional[Item]]] = None):
        super().__init__(key_field)
        self.__backup_fetch = backup_fetch_func

    def generate(self, key: str) -> Item:
        if self.__backup_fetch is not None:
            return self.__backup_fetch(key)
        return None
    
    def gen_item(self, key: str) -> Item:
        # Check if item is already in cache
        item = self.fetch_item(key)
        if item:
            return item

        item = self.generate(key)
        stored_item = self.store_item(item)
        return stored_item

    def __call__(self, key: str) -> Optional[Item]:
        return self.gen_item(key)
    
# _backup_fetch

# Cache Fetch
# look at cache
# 
# Cache Store
# fetch from cache
# if empty store
# 

# SingletonCache
# fetch
# if empty 
#   generate
#   store result in cache
# 
