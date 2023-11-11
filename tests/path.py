from scrapy.selector import Selector, SelectorList # type: ignore

def element_path(selector):
    # If a SelectorList is passed, get the first Selector
    if isinstance(selector, SelectorList):
        if not selector:
            return []  # Return an empty path if the selector list is empty
        selector = selector[0]
    
    path = []
    # Use root to access the lxml element wrapped by the Selector
    element = selector.root
    while element is not None and element.tag is not None:
        parent = element.getparent()
        siblings = parent.getchildren() if parent is not None else []
        index = siblings.index(element) + 1 if element in siblings else 0
        path.insert(0, (element.tag, index))
        element = parent
    
    return path

# Example usage within a Scrapy spider or shell
html_content = """
<html>
    <body>
        <div>
            <header>Header Content</header>
            <nav>Nav Content</nav>
            <article>
                <section>
                    <aside>Sidebar Content</aside>
                </section>
            </article>
            <footer>Footer Content</footer>
        </div>
    </body>
</html>
"""

selector = Selector(text=html_content)
header_selector = selector.xpath('//nav')  # This will return a SelectorList
header_path = element_path(header_selector)

print(header_path)
