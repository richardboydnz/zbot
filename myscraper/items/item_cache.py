from typing import Callable, Dict, Optional
from scrapy import Item  # type: ignore
from typing import TypeVar, Generic

T = TypeVar('T')

class ItemCache(Generic[T]):
    def __init__(self, key_field: str):
        self.cache: Dict[T, Item] = {}  # Cache to store Item objects
        self.key_field = key_field  # Key field for identifying items

    def fetch_item(self, key: T) -> Item:
        # Check if item is already in cache
        item = self.cache.get(key)
        return item

    def update_item(self, cachedItem: Item, newItem: Item):
        pass

    def store_item(self, item: Item) -> Item:
        key: T = item[self.key_field]
        cached_item = ItemCache.fetch_item(self,key)
        if cached_item is not None:
            self.update_item(cached_item, item)
        else:
            self.cache[key] = item
        return item

class GeneratorCache(ItemCache[T]):
    def __init__(self, key_field: str, backup_fetch_func: Optional[Callable[[T], Optional[Item]]] = None):
        super().__init__(key_field)
        self.__backup_fetch = backup_fetch_func

    def generate(self, key: T) -> Item:
        if self.__backup_fetch is not None:
            return self.__backup_fetch(key)
        return None
    
    def gen_item(self, key: T) -> Item:
        # Check if item is already in cache
        item = self.fetch_item(key)
        if item:
            return item

        item = self.generate(key)
        if item is not None:
            item = self.store_item(item)
        return item

    def __call__(self, key: T) -> Optional[Item]:
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
