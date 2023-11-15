from ..items import DomainItem

class DomainFactory:
    def __init__(self):
        self.domains_cache = {}  # Cache to store DomainItem objects keyed by domain name

    def get_domain_item(self, domain_name):
        if domain_name not in self.domains_cache:
            # Create a new DomainItem if not in cache
            domain_item = DomainItem(domain_name=domain_name)
            self.domains_cache[domain_name] = domain_item
        return self.domains_cache[domain_name]

    def get_domain_id(self, domain_name):
        domain_item = self.domains_cache.get(domain_name)
        return domain_item['domain']_id if domain_item else None

    def update_domain_id(self, domain_name, domain_id):
        if domain_name in self.domains_cache:
            self.domains_cache[domain_name].domain_id = domain_id

if __name__ == "__main__":

    # Example Usage
    domain_factory = DomainFactory()
    domain_item = domain_factory.get_domain_item('example.com')
    # Later, update the domain_id when it is available
    domain_factory.update_domain_id('example.com', 123)
