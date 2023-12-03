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
        cachedItem = ItemCache.fetch_item(self, key)
        if cachedItem is not None:
            self.update_item(cachedItem, item)
        else:
            self.cache[key] = item
        return item

class SingletonCache(ItemCache):
    def __init__(self, key_field: str, backup_fetch_func: Callable[[str], Optional[Item]]):
        super().__init__(key_field)
        self.__backup_fetch = backup_fetch_func

    def fetch_item(self, key: str) -> Item:
        # Check if item is already in cache
        item = super().fetch_item(key)
        if item:
            return item

        item = self.__backup_fetch(key)
        self.store_item(item)
        return item

    def __call__(self, key: str) -> Optional[Item]:
        return self.fetch_item(key)
# _backup_fetch