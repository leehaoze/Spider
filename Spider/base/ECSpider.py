# -*- coding: utf-8 -*-
from Spider.base.base_spider import BaseSpider


class ECSpider(BaseSpider):
    def start_requests(self):
        for url in self.start_urls:
            yield self.splash_request(url=url, callback=self.parse_navigation)

    def parse_navigation(self, response):
        ul = response.xpath('//li')
        for li in ul:
            tag_a = li.xpath('./a[@href]')
            for link in tag_a:
                text = link.xpath('normalize-space(.)')[0].extract()
                if len(text) <= 4:
                    url = link.xpath('.//@href')[0]
                    if not url.re('^https:'):
                        url = 'https:' + url.extract()
                    else:
                        url = url.extract()
                    yield self.splash_request(url=url, callback=self.parse)

    def parse(self, response):
        raise NotImplementedError

