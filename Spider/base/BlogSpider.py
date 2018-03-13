# -*- coding: utf-8 -*-

from Spider.base.base_spider import BaseSpider

class BlogSpider(BaseSpider):
    def start_requests(self):
        for url in self.start_urls:
            yield self.splash_request(url=url, callback=self.parse)

    def parse(self, response):
        raise NotImplementedError