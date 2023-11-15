from scrapy import Item  # type: ignore


class ItemCache:
    def __init__(self):
        self.cache = {}  # Cache to store URLItem objects

    def _make_item(self, key:str):
        pass

    def get_item(self, key:str) -> Item:
        # Check if URL is already in cache
        if key not in self.cache:
            self.cache[key] = self._make_item(key)

        return self.cache[key]
    
    def get_id(self, url_name: str):
        url_item = self.cache.get(url_name)
        return url_item['url_id'] if url_item else None

    def update_id(self, key: str, id: int):
        if key in self.cache:
            self.cache[key].url_id = id