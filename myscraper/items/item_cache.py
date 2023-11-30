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

    def store_item(self, item: Item):
        key = item[self.key_field]
        cachedItem = self.fetch_item(key)
        if cachedItem is not None:
            self.update_item(cachedItem, item)
        else:
            self.cache[key] = item

class SingletonCache(ItemCache):
    def __init__(self, key_field: str, create_singleton_func: Callable[[str], Optional[Item]]):
        super().__init__(key_field)
        self._create_singleton = create_singleton_func

    def fetch_item(self, key: str) -> Item:
        # Check if item is already in cache
        item = super().fetch_item(key)
        if item:
            return item

        item = self._create_singleton(key)
        self.store_item(item)
        return item
