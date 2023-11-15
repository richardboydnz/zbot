from myscraper.items.item_cache import ItemCache
from . import UrlItem
from urllib.parse import urlparse

class URLCache(ItemCache):
    # def __init__(self):
    #     self.cache = {}  # Cache to store URLItem objects

    def _make_item(self, key:str):
        # Parse the URL
        parsed_url = urlparse(key)
        protocol = parsed_url.scheme
        domain = parsed_url.netloc
        path = parsed_url.path

        path_segments = path.split('/')
        last_path_segment = path_segments[-1] if path_segments else ''
        file_parts = last_path_segment.split('.')
        # Choose the last part as the file extension if there are multiple parts, otherwise set to empty string
        file_extension = file_parts[-1] if len(file_parts) > 1 else ''

        # Determine if it is a resource or navigable
        is_resource = file_extension != '' and file_extension not in ['html', 'htm', 'php', 'asp', 'aspx', 'jsp']
        is_webpage = not is_resource

        # Create a new URLItem
        return UrlItem(
            url=key,
            protocol=protocol,
            domain=domain,
            path=path,
            is_resource=is_resource,
            is_webpage=is_webpage,
            resource_type='',  # This would be determined later
            last_status_code=0,  # This would be updated later
            file_extension=file_extension
        )

    # def get_item(self, key:str) -> UrlItem:
    #     # Check if URL is already in cache
    #     if key not in self.cache:
    #         self.cache[key] = self._make_item(key)

    #     return self.cache[key]
    
    # def get_id(self, url_name: str):
    #     url_item = self.cache.get(url_name)
    #     return url_item['url_id'] if url_item else None

    # def update_id(self, url_name: str, url_id: int):
    #     if url_name in self.cache:
    #         self.cache[url_name].url_id = url_id


# if __name__ == "__main__":

#     # Example usage:
#     url_cache = URLCache()
#     url_item = url_cache.get_item('http://www.example.com/page.html')
