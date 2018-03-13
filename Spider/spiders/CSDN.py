# -*- coding: utf-8 -*-
from Spider.base.base_spider import BaseSpider
from Spider.base.BlogSpider import BlogSpider
from Spider.analysts.analyst import CSDNBlog


class CSDNSpider(BlogSpider):
    name = 'CSDN'
    analyst = CSDNBlog()

    def parse(self, response):
        url = response.xpath('//a[@href]')
        for each in url:
            link = each.xpath('.//@href')[0]
            if not link.re('^http'):
                next_url = 'https:' + link.extract()
            else:
                next_url = link.extract()
            yield self.pass_response(response)
            yield self.splash_request(next_url, self.parse)

    def pass_response(self, response):
        return self.analyst.parse(response)