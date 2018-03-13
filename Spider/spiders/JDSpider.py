# -*- coding: utf-8 -*-
from Spider.base.ECSpider import ECSpider
from Spider.analysts.analyst import JDAnalyst
from scrapy_splash import SplashRequest


class JDSpider(ECSpider):
    name = 'JDSpider'
    analyst = JDAnalyst()

    def parse(self, response):
        print 'download success : ' + response.xpath('normalize-space(/html/head/title)')[0].extract()
        url = response.xpath('//a[@href]')
        for each in url:
            link = each.xpath('.//@href')[0]
            if link.re('jd.com'):
                if not link.re('^http'):
                    next_url = 'https:' + link.extract()
                else:
                    next_url = link.extract()
                yield self.splash_request(next_url, callback=self.pass_response)
                yield self.splash_request(next_url, callback=self.parse)


    def pass_response(self, response):
        return self.analyst.parse(response)