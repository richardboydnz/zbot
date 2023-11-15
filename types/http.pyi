# This is an example stub file for Scrapy's Response object

from typing import Dict, List, Optional, Union, Any, Type, Callable
import ipaddress
from twisted.internet.ssl import Certificate
from scrapy.http import Request, FormRequest # type: ignore
from scrapy.selector import Selector, SelectorList # type: ignore
# from scrapy.http import Response

class Response:
    url: str
    status: int
    headers: Dict[bytes, List[bytes]]
    body: bytes
    flags: List[str]
    request: Optional[Request]
    certificate: Optional[Certificate]
    ip_address: Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]
    protocol: Optional[str]

    def __init__(self, url: str, status: int = 200, headers: Optional[Dict[bytes, List[bytes]]] = None, body: bytes = b'', flags: Optional[List[str]] = None, request: Optional[Request] = None, certificate: Optional[Certificate] = None, ip_address: Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]] = None, protocol: Optional[str] = None) -> None: ...
    
    def copy(self) -> 'Response': ...
    def replace(self, url: Optional[str] = None, status: Optional[int] = None, headers: Optional[Dict[bytes, List[bytes]]] = None, body: Optional[bytes] = None, request: Optional[Request] = None, flags: Optional[List[str]] = None, cls: Optional[Type['Response']] = None) -> 'Response': ...
    def urljoin(self, url: str) -> str: ...
    def follow(self, url: Union[str, Selector, SelectorList], callback: Optional[Callable[..., Any]] = None, meta: Optional[Dict[str, Any]] = None, **kwargs: Any) -> FormRequest: ...

class TextResponse(Response):
    encoding: str
    selector: Optional[SelectorList]
    text: str

    def __init__(self, url: str, encoding: Optional[str] = None, status: int = 200, headers: Optional[Dict[bytes, List[bytes]]] = None, body: Union[bytes, str] = b'', flags: Optional[List[str]] = None, request: Optional[Request] = None) -> None: ...
    
    def xpath(self, query: str, **kwargs: Any) -> SelectorList: ...
    def css(self, query: str, **kwargs: Any) -> SelectorList: ...
    def jmespath(self, query: str) -> Any: ...
    def json(self) -> Any: ...

class HtmlResponse(TextResponse):
    pass

class XmlResponse(TextResponse):
    pass

class JsonRequest(Request):
    # Additional attributes and methods for JsonRequest
    pass
