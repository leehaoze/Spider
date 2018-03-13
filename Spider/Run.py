# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector

import redis

import pymongo
import threading
import json
import shutil
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def UI():
    print 'Choose type of the page:\n1.电商\n2.博客\n3.本地测试网页\n'
    order = input()
    if order is 1:
        print '1.京东\n'
        order = input()
        if order is 1:
            run('JDSpider')
    elif order is 2:
        print '1.CSDN\n'
        order = input()
        if order is 1:
            run('CSDN')
    else:
        local()


def local():
    # path = '/Users/leehaoze/Desktop/TEST_DATA/DATA'
    print 'Please input the path of Pages\n'
    path = raw_input()
    files = os.listdir(path)
    parent_path = os.path.dirname(path)
    if os.path.exists(parent_path + "/Output"):
        print "文件夹已存在,将要清空文件夹\n"
        shutil.rmtree(parent_path + "/Output")
        os.mkdir(parent_path + '/Output')
    else:
        print "结果将输出到同目录的Output下\n"
        os.mkdir(parent_path + '/Output')
    for file in files:
        if file == ".DS_Store":
            continue
        try:
            print file
            f = open(path + "/" + file)

            if file.find('blog_') is 0:
                rec = Selector(text=f.read()).xpath('string(//div[@id="sina_keyword_ad_area2"])')[0].extract()
            elif file.startswith('BN') or file.startswith('CL') or file.startswith('CM'):
                rec = Selector(text=f.read()).xpath('string(//div[@class="post_text"])')[0].extract()
            else:
                rec = Selector(text=f.read()).xpath('string(//div[@id="Cnt-Main-Article-QQ"])')[0].extract()
        except:
            rec = 'Error'
        file = open(parent_path + "/Output/" + file, 'w', 1)
        file.write(rec)
        file.close()


from scrapy.conf import settings


def insert(self, item, collection_name=None):
    '''
    插入数据，这里的数据可以是一个，也可以是多个
    :param item: 需要插入的数据
    :param collection_name:  可选，需要访问哪个集合
    :return:
    '''
    if collection_name != None:
        collection = self.db.get_collection(self.db)
        collection.insert(item)
    else:
        self.collection.insert(item)


def find(self, expression=None, collection_name=None):
    '''
    进行简单查询，可以指定条件和集合
    :param expression: 查询条件，可以为空
    :param collection_name: 集合名称
    :return: 所有结果
    '''
    if collection_name != None:
        collection = self.db.get_collection(self.db)
        if expression == None:
            return collection.find()
        else:
            return collection.find(expression)
    else:
        if expression == None:
            return self.collection.find()
        else:
            return self.collection.find(expression)


def get_collection(self, collection_name=None):
    '''
    很多时候单纯的查询不能够通过这个类封装的方法执行，这时候就可以直接获取到对应的collection进行操作
    :param collection_name: 集合名称
    :return: collection
    '''
    if collection_name == None:
        return self.collection
    else:
        return self.get_collection(collection_name)


def write_to_database(func):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])

    # 数据库登录需要帐号密码的话

    # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])

    db = client[func]  # 获得数据库的句柄

    # coll = db[settings['MONGO_COLL']]  # 获得collection的句柄

    print '子线程简建立\n'

    while True:
        # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
        source, data = r.blpop([func + ":items"])
        Item = json.loads(data)
        item = dict(Item)
        coll = db['Data']
        coll.insert(item)


def run(name):
    # 获取settings.py模块的设置
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)

    # 可以添加多个spider
    process.crawl(name)

    t = threading.Thread(target=write_to_database, args=(name,))
    t.setDaemon(True)
    t.start()
    # 启动爬虫，会阻塞，直到爬取完成
    process.start()

UI()
