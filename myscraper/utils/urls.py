from ..items import UrlItem
from urllib.parse import urlparse

class URLCache:
    def __init__(self):
        self.urls_cache = {}  # Cache to store URLItem objects

    def get_url_item(self, url:str):
        # Check if URL is already in cache
        if url in self.urls_cache:
            return self.urls_cache[url]

        # Parse the URL
        parsed_url = urlparse(url)
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
        is_navigable = not is_resource

        # Create a new URLItem
        url_item = UrlItem(
            url=url,
            protocol=protocol,
            domain=domain,
            path=path,
            is_resource=is_resource,
            is_navigable=is_navigable,
            resource_type='',  # This would be determined later
            last_status_code=0,  # This would be updated later
            file_extension=file_extension
        )

        # Store in cache
        self.urls_cache[url] = url_item

        return url_item
    
    def get_url_id(self, url_name: str):
        url_item = self.urls_cache.get(url_name)
        return url_item.url_id if url_item else None

    def update_url_id(self, url_name: str, url_id: int):
        if url_name in self.urls_cache:
            self.urls_cache[url_name].url_id = url_id


if __name__ == "__main__":

    # Example usage:
    url_cache = URLCache()
    url_item = url_cache.get_url_item('http://www.example.com/page.html')
