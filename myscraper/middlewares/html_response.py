from scrapy.http import HtmlResponse

class CustomMiddleware:
    def process_request(self, request, spider):
        if request.method == 'HTML':
            fragment = request.meta['fragment']
            return HtmlResponse(
                url=request.url,
                body=fragment,
                encoding='utf-8',
                request=request
            )
        # Returning None for other requests to continue normal processing
