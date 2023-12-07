import pytest
from scrapy.http import Request # type: ignore
from scrapy.http import HtmlResponse
from myscraper.db.init_db import get_db

from myscraper.items import ContentItem, HtmlContentItem, HtmlItem, DownloadItem
from myscraper.settings import DB_SETTINGS
from myscraper.spiders.website_spider import WebsiteSpider
from myscraper.encode.hash import hash64
from .example import example_html
# from myscraper.parsers.fragment_parser import Fragment_Parser  

import pytest
from bs4 import BeautifulSoup

def test_html_roundtrip():
    # example_html = """<!DOCTYPE html>
    # <html manifest="site.manifest">
    # <head>
    #     <title>My Complex Web Page</title>
    #     <!-- Additional head content -->
    # </head>
    # <body>
    #     <!-- Body content -->
    #     <footer>
    #         <p>© 2023 My Complex Web Page. All rights reserved.</p>
    #     </footer>
    # </body>
    # </html>
    # """

    url = "http://example.com"
    response = HtmlResponse(url=url, body=example_html, encoding='utf-8')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the footer content
    extracted_footer = str(soup.footer)

    # Define the expected footer content
    expected_footer = "<footer>\n<p>© 2023 My Complex Web Page. All rights reserved.</p>\n</footer>"

    # Assert that the extracted footer matches the expected footer
    assert extracted_footer == expected_footer

def test_db():
    db_settings = DB_SETTINGS
    db = get_db(db_settings)


def test_parse_item():
    # Create a fake response object
    url = 'http://example.com'
    response = HtmlResponse(url=url, body=example_html, encoding='utf-8')
    # Instantiate the spider and call find_fragments
    spider = WebsiteSpider(domain_name='example.com')

    items = spider.parse_item(response)

    html_hash = ""
    for item in items:
        if isinstance(item, HtmlItem):
            print("HtmlItem ------------------")
            print(item)
            html_hash = item['html_hash']

            assert item['html_data'] == example_html
        elif isinstance(item, DownloadItem):
            print("DownloadItem ------------------")
            print(item)

            assert item['url'] == url
            assert item['html_hash'] == html_hash
        elif isinstance(item, Request):
            request = item
            print("content ------------------")
            print( request.method, request.url )
            print(request.meta['content'])
            assert request.meta['content'] in [footer, nav, header, aside, main]

def test_parse_fragment():
    url = 'http://example.com'
    orig_response = HtmlResponse(url=url, body=example_html, encoding='utf-8')
    response = HtmlResponse(url=url, body=main, encoding='utf-8')
    # Instantiate the spider and call find_fragments
    spider = WebsiteSpider()

    html_hash = hash64(example_html)
    fragment_text = main
    content_hash = hash64(main)
    content_type = 'html'

    items = spider.parse_fragment(response, orig_response=orig_response, 
                                  html_hash=html_hash, content_type=content_type, path = "")

    content_hash = ""
    for item in items:
        print( item.__class__.__name__, ' ------------------------------------')
        print( item )
        if isinstance(item, ContentItem):
            content_hash = item['content_hash']
            assert item['content_hash'] == content_hash
        elif isinstance(item, HtmlContentItem):
            assert item['content_hash'] == content_hash
            assert item['html_hash'] == html_hash
        # elif isinstance(item, Request):
        #     print("fragment ------------------")
        #     print(item)


    pass
    # Assertions or checks on the fragments
    # assert 'header' in fragments
    # assert 'footer' in fragments
    # Add more checks as needed


# def test_get_fragments():
#     # Create a fake response object
#     # response = HtmlResponse(url='http://example.com', body=example_html, encoding='utf-8')

#     # Instantiate the spider and call find_fragments
#     spider = WebsiteSpider()
#     fragments = get_fragments(example_html)

#     for frag, _, _ in fragments:
#         print("------------------")
#         print(frag)
#         assert str(frag) in [nav, header, footer, aside, main]



    # Assertions or checks on the fragments
    # assert 'header' in fragments
    # assert 'footer' in fragments
    # Add more checks as needed


nav = """<nav>
<a href="page1.html">Home</a>
<a href="page2.html">About Us</a>
<a href="page3.html">Services</a>
<a href="page4.html">Contact</a>
</nav>"""
header = """<header>
<h1>Welcome to My Web Page</h1>

</header>"""
footer = """<footer>
<p>© 2023 My Complex Web Page. All rights reserved.</p>
</footer>"""
aside = """<aside>
<h3>Special Offer!</h3>
<p>Don't miss our exclusive offer at <a href="https://www.example.com" ping="tracker.php">Example.com</a></p>
</aside>"""
main = """<!DOCTYPE html>

<html manifest="site.manifest">
<head>
<title>©My Complex Web Page</title>
<script src="script.js"></script>
<style>
        body { background: url('background.jpg'); }
        header, footer { background: lightgray; padding: 10px; text-align: center; }
        nav a { margin: 0 10px; }
        aside { background: #f0f0f0; padding: 10px; }
        main { padding: 20px; }
        video, img, audio, object { display: block; margin-top: 20px; }
    </style>
</head>
<body>


<main>
<section>
<h2>Our Mission</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
<iframe height="200" src="frame.html" width="300"></iframe>
<iframe height="200" srcdoc="&lt;p&gt;Inline HTML content here.&lt;/p&gt;" width="300"></iframe>
</section>
<article>
<h2>Featured Content</h2>
<video controls="" poster="poster.jpg" width="400">
<source src="video.mp4" type="video/mp4"/>
<track kind="subtitles" label="English" src="subtitles_en.vtt" srclang="en"/>
                Your browser does not support the video tag.
            </video>
<img alt="Image with Map" src="photo.jpg" srcset="photo.jpg 1x, photo@2x.jpg 2x" usemap="#imagemap" width="400"/>
<map name="imagemap">
<area alt="Linked Area" coords="34,44,270,350" href="linked.html" shape="rect"/>
</map>
<audio controls="" src="audio.mp3">Your browser does not support the audio element.</audio>
<object data="embedded.swf" height="300" type="application/x-shockwave-flash" width="400">Flash content cannot be displayed.</object>
</article>
</main>

</body>
</html>
"""

# Run the test
# test_find_fragments()
# if __name__ == "__main__":
#     test_get_fragments()