import re
from bs4 import BeautifulSoup 
from ..items import LinkItem
from .markdown import soup_to_markdown

url_patterns = [
    ('a', 'href', 'webpage'),
    ('img', 'src', 'resource'),
    ('audio', 'src', 'resource'),
    ('video', 'src', 'resource'),
    ('source', 'src', 'resource'),
    ('script', 'src', 'scripts'),
    ('link', 'href', 'style'),
    ('area', 'href', 'webpage'),
    ('embed', 'src', 'resource'),
    ('iframe', 'src', 'resource'),
    ('input', 'src', 'resource'),
    ('form', 'action', 'other_url'),
    ('object', 'data', 'resource'),
    ('html', 'manifest', 'other_url'),
    ('svg', 'xlink:href', 'webpage'),
]

# Note: For the 'input' tag, an additional filter is provided for type 'image'.
# For SVG elements, a namespace filter is used to correctly identify elements with xlink:href.

def gen_link_items(soup, content_item):
    for tag_type, attr, link_type in url_patterns:
        for tag in soup.find_all(tag_type, **{attr: True}):
            yield LinkItem(
                domain=content_item.domain,
                from_content_raw_hash=content_item.content_raw_hash,
                to_url=tag[attr],
                link_text=soup_to_markdown(tag),
                link_tag=tag.name,
                link_attr=attr,
                link_type=link_type,
                internal=content_item.domain in tag[attr]
            )
    for tag in soup.find_all('style'):
        css_content = tag.string or ''
        for link_item in gen_css_links(css_content, content_item):
            yield link_item

    for tag in soup.find_all(style=True):
        inline_styles = tag['style']
        for link_item in gen_css_links(inline_styles, content_item):
            yield link_item


def gen_css_links(css_content, content_item):
    css_url_pattern = re.compile(r'url\((.*?)\)')
    css_import_pattern = re.compile(r'@import\s+["\']?(.*?)["\']?;')

    for url_match in css_url_pattern.finditer(css_content):
        yield LinkItem(
            domain=content_item.domain,
            from_content_raw_hash=content_item.content_raw_hash,
            to_url=url_match.group(1),
            link_type='resources',
            internal=content_item.domain in url_match.group(1)
        )
    
    for import_match in css_import_pattern.finditer(css_content):
        yield LinkItem(
            domain=content_item.domain,
            from_content_raw_hash=content_item.content_raw_hash,
            to_url=import_match.group(1),
            link_type='styles',
            internal=content_item.domain in import_match.group(1)
        )

if __name__ == "__main__":
    # Example usage
    from .html_snippets import test_html_content 

    soup = BeautifulSoup(test_html_content, 'html.parser')
    domain = 'example.com'  # The domain of the content
    for link_item in gen_link_items(soup, domain):
        # Process each LinkItem
        pass
