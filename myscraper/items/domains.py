from myscraper.items.item_cache import ItemCache 
from . import DomainItem

class DomainCache(ItemCache):
    # def __init__(self):
    #     self.cache = {}  # Cache to store DomainItem objects keyed by domain name

    def _make_item(self, key:str):
        return DomainItem(domain_name=key)
    
    # def get_item(self, key):
    #     if key not in self.cache:
    #         # Create a new DomainItem if not in cache
    #         domain_item = DomainItem(domain_name=key)
    #         self.cache[key] = self._make_item(key)
    #     return self.cache[key]

    # def get_id(self, key):
    #     domain_item = self.cache.get(key)
    #     return domain_item['domain_id'] if domain_item else None

    # def update_id(self, key, id):
    #     if key in self.cache:
    #         self.cache[key].domain_id = id

# if __name__ == "__main__":

#     # Example Usage
#     domain_factory = DomainFactory()
#     domain_item = domain_factory.get_item('example.com')
#     # Later, update the domain_id when it is available
#     domain_factory.update_id('example.com', 123)
