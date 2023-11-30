from scrapy.http import HtmlResponse # type: ignore

class CustomMiddleware: 
    # connect to db, look for fragment in db - do not process if exists.
    # use db cache - populate hash - id for dependants
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
