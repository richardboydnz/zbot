# utils/markdown.py

from markdownify import MarkdownConverter # type: ignore
from bs4 import BeautifulSoup # type: ignore
from typing import Optional

import re

class StandardMarkdownConverter(MarkdownConverter):
    def __init__(self, **options):
        super().__init__(heading_style='ATX', **options)

class NoLinkMarkdownConverter(StandardMarkdownConverter):
    def convert_a(self, el, text: str, convert_as_inline: bool) -> str:
        return text
    
def soup_to_markdown(soup: BeautifulSoup, links: bool = True, **options) -> str:
    """
    Converts BeautifulSoup fragment to markdown.
    If no_links is True, links will not be included in the markdown output.
    """
    if links:
        converter = StandardMarkdownConverter(**options)
    else:
        converter = NoLinkMarkdownConverter(**options)

    return clean_text(converter.convert_soup(soup))

def clean_text(text: str) -> str:
    # Collapse multiple whitespace into a single whitespace
    text = re.sub(r'\t+', ' ', text)
    # collapse multiple spaces into a single space within each line of a string, after the first space
    text = re.sub(r'(?<!\n)( ){2,}', ' ', text, flags=re.MULTILINE)
    # Delete spaces at the end of each line (leading spaces may be semantic)
    text = re.sub(r' $', '', text, flags=re.MULTILINE)
    # Remove newlines at the beginning and end of the string
    #   must happen after trailing spaces are dealt with
    text = text.strip('\n')
    # Collapse more than two newlines into a single blank line
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text



    
# Additional utility functions can be added here as needed


# utils/markdown.py

# ... [rest of your markdown.py file code] ...

if __name__ == "__main__":
    # This block will only execute if this file is run directly from the CLI
    # It will not run when this module is imported elsewhere


    # Example HTML content
    html_content = '''
    <div>
        <h1>Example  Header</h1>
        <p>This is a paragraph 
        

        with <a href="http://example.com">a    link</a>.</p>
        <p>This is another paragraph, without a link.</p>
    </div>
    '''

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Convert to markdown with links
    print(html_content)
    markdown_with_links = soup_to_markdown(soup)
    print("Markdown with links:")
    print(markdown_with_links)
    print("---")

    # Convert to markdown without links
    markdown_without_links = soup_to_markdown(soup, no_links=True)
    print("Markdown without links:")
    print(markdown_without_links)
    print("---")

    # Show cleaned text
    cleaned_text = clean_text(markdown_with_links)
    print("Cleaned text:")
    print(cleaned_text)
    print("---")
