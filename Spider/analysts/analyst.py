# -*- coding: utf-8 -*-
import urllib2
from Spider.items import JDProductItem
from Spider.items import JDPage
from Spider.items import CSDNArticle
import time
import json
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Analyst:
    allowed_domains = []
    start_urls = []

    def __init__(self, allowed_domains=None, start_urls=None):
        if allowed_domains is not None:
            self.allowed_domains = allowed_domains
        elif not getattr(self, 'allowed_domains', None):
            raise ValueError("%s must have a allowed_domains" %
                             type(self).__name__)

        if start_urls is not None:
            self.start_urls = start_urls
        elif not getattr(self, 'start_urls', None):
            raise ValueError("%s must have a start_urls" %
                             type(self).__name__)

    def parse(self, response):
        raise NotImplementedError

class JDAnalyst(Analyst):
    allowed_domains = ['jd.com']
    start_urls = [
        'https://item.jd.com/2168838.html',
        'https://item.jd.com/4663790.html',
        'https://item.jd.com/4453528.html',
        'https://item.jd.com/3995643.html',
        'https://item.jd.com/3553539.html',
        'https://item.jd.com/1978758.html',
        'https://item.jd.com/12128352.html',
        'https://item.jd.com/11963485.html',
        'https://item.jd.com/12116784.html',
        'https://item.jd.com/1644293422.html?cpdad=1DLSUE#none'
    ]

    def get_product_id(self, url):
        re_product_id = re.compile(r'(?<=/)\d*(?=.html)')
        product_id = re_product_id.findall(url)[0]
        return product_id

    def get_product_name(self, product_id):
        try:
            url = 'https://question.jd.com/question/getQuestionAnswerList.action?callback=jQuery8259178&page=1&productId=' + str(
                product_id)
            response = urllib2.urlopen(url).read()
            data = re.findall(r'(?<=\(){.*}(?=\))', response)[0].decode("utf-8")
            data = json.loads(data)
            return data['skuInfo']['fullName']
        except:
            return "Error"

    def get_product_price(self, product_id):
        try:
            url = 'https://p.3.cn/prices/mgets?callback=jQuery4972697&type=1&area=1_72_4137_0&pdtk=&pduid=14928752733061601620339&pdpin=&pdbp=0&skuIds=J_' + str(
                product_id) + '&source=item-pc'
            response = urllib2.urlopen(url).read()
            data = re.findall(r'(?<=\(\[){.*}(?=\]\);)', response)[0]
            data = json.loads(data)
            return data['p']
        except:
            return "Error"

    def get_store_info(self, product_id):
        try:
            url = 'https://chat1.jd.com/api/checkChat?&callback=jQuery5248355&pid=10822586485&returnCharset=utf-8&_=' + product_id
            response = urllib2.urlopen(url).read()
            data = re.findall(r'(?<=\(){.*}(?=\))', response)[0].decode("GB18030")
            data = json.loads(data)
            return [data['shopId'], data['seller']]
        except:
            return "Error"

    def get_proudct_info(self, response):
        try:
            ul = response.xpath('//ul[@id="parameter2"] | //ul[@class="parameter2 p-parameter-list"]')
            info = ""
            for each in ul:
                info += each.xpath('normalize-space(.)')[0].extract()
            return info
        except:
            return "Error"

    def get_comment(self, product_id):
        try:
            comment_info = urllib2.urlopen(
                'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv18058&productId=' + str(
                    product_id) + '&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0')
            limit = re.compile(r'(?<=\(){.*}(?=\);)')
            ans = limit.findall(comment_info.read())[0].decode('GB18030')
            data = json.loads(ans)
            item = [data['productCommentSummary']['goodRateShow'], data['productCommentSummary']['afterCountStr'],
                    data['productCommentSummary']['generalCountStr'], data['productCommentSummary']['goodCountStr'],
                    data['productCommentSummary']['poorCountStr']]
            length = len(data['hotCommentTagStatistics'])
            item.append("")
            for i in range(0, length - 1):
                item[5] += data['hotCommentTagStatistics'][i]['name'] + '\n'

            return item
        except:
            return "Error"

    def parse(self, response):
        url = response.url
        if re.search(r'item.jd.com', url):
            return self.parse_product(response)
        else:
            return self.parse_page(response)

    def parse_page(self, response):
        item = JDPage()
        item['type'] = 'JDPage'
        item['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        item['title'] = response.xpath('normalize-space(/html/head/title)')[0].extract()
        item['url'] = response.url
        return item

    def parse_product(self, response):
        item = JDProductItem()
        item['type'] = 'JDProductItem'
        item['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        id = self.get_product_id(response.url)
        item['product_id'] = id
        item['name'] = self.get_product_name(id)
        item['price'] = self.get_product_price(id)

        store_info = self.get_store_info(id)
        store_id = store_info[0]
        store_name = store_info[1]

        item['store_name'] = store_name
        item['store_id'] = str(store_id)
        item['product_info'] = self.get_proudct_info(response)

        comment_info = self.get_comment(id)
        item['good_rate'] = str(comment_info[0])
        item['after_comment'] = str(comment_info[1])
        item['medium_comment'] = str(comment_info[2])
        item['good_comment'] = str(comment_info[3])
        item['bad_comment'] = str(comment_info[4])
        item['product_tags'] = str(comment_info[5])

        print 'crawl_time : ' + item['crawl_time']
        print 'product_id : ' + item['product_id']
        print 'name : ' + item['name']
        print 'price : ' + item['price']
        print 'store_name : ' + item['store_name']
        print 'store_id : ' + item['store_id']
        print 'product_info : ' + item['product_info']
        print 'good_rate : ' + item['good_rate']
        print 'after_comment : ' + item['after_comment']
        print 'medium_comment : ' + item['medium_comment']
        print 'good_commen : ' + item['good_comment']
        print 'bad_comment : ' + item['bad_comment']
        print 'product_tags : ' + item['product_tags']

        return item

class CSDNBlog(Analyst):
    allowed_domains = ["blog.csdn.net"]
    start_urls = ["http://blog.csdn.net/"]

    def parse_article(self, response):
        title = response.xpath('normalize-space(/html/head/title)')[0].extract()
        author = response.xpath('string(//a[@class="user_name"])')[0].extract()
        content = response.xpath('string(//div[@id="article_content"])')[0].extract()
        content = content[0:-561] + '\n'
        item = CSDNArticle()
        item['title'] = title
        item['author'] = author
        item['content'] = content
        return item

    def parse_news(self, response):
        title = response.xpath('//*[@id="newest"]/div/dl/dd/h2/span')[0].extract()
        description = response.xpath('string(//blockquote/p)')[0].extract()
        p = response.xpath('//div[@class="description markdown_views clearfix"]/p')
        content = None
        for each in p:
            content += each.xpath('string(.)')[0].extract()
        item = CSDNArticle()
        item['title'] = title
        item['description'] = description
        item['content'] = content
        return item

    def parse(self, response):
        if re.search(r'article', response.url):
            return self.parse_article(response)
        elif re.search(r'news', response.url):
            return self.parse_news(response)




