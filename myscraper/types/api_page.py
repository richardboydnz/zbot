from typing import List, Optional
from typing_extensions import TypedDict

class Guid(TypedDict):
    rendered: str

class Title(TypedDict):
    rendered: str

class Content(TypedDict):
    rendered: str
    protected: bool

from typing import TypedDict, List, Optional

class LinkItem(TypedDict, total=False):
    href: str
    embeddable: Optional[bool]
    count: Optional[int]

class CuriesItem(TypedDict):
    name: str
    href: str
    templated: bool

from typing_extensions import TypedDict

Links = TypedDict('Links', {
    'self': List[LinkItem],
    'collection': List[LinkItem],
    'about': List[LinkItem],
    'author': List[LinkItem],
    'replies': List[LinkItem],
    'version-history': List[LinkItem],
    'wp:attachment': List[LinkItem],
    'curies': List[CuriesItem]
})

class Meta(TypedDict):
    _et_pb_use_builder: str
    _et_pb_old_content: str
    _et_gb_content_width: str

class Page(TypedDict):
    id: int
    date: str
    date_gmt: str
    guid: Guid
    modified: str
    modified_gmt: str
    slug: str
    status: str
    type: str
    link: str
    title: Title
    content: Content
    excerpt: Content
    author: int
    featured_media: int
    parent: int
    menu_order: int
    comment_status: str
    ping_status: str
    template: str
    meta: Meta
    _links: Links

# This represents the data you get from response.json(), which is a list of Page objects.

Pages = List[Page]
