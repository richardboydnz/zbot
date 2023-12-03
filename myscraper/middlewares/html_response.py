import logging
from scrapy.http import HtmlResponse # type: ignore

class HandleHtmlFragmentRequest: 
    # connect to db, look for fragment in db - do not process if exists.
    # use db cache - populate hash - id for dependants
    def process_request(self, request, spider):
        logging.debug(f'---- HandleHtmlFragementRequest ---, request URL: {request.url}')

        print("---- HandleHtmlFragementRequest ---", request)
        if request.method == 'HTML':
            fragment = request.meta['fragment']
            return HtmlResponse(
                url=request.url,
                body=fragment,
                encoding='utf-8',
                request=request
            )
        return None
        # Returning None for other requests to continue normal processing
