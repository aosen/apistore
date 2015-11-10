# coding=utf-8

import json
import time
import datetime
from urlparse import urlparse

import scrapy

from robot.items import RobotItem
from robot.models.base import Base
from robot.settings import logger

class WwwToutiaoComItem(RobotItem):
    title = scrapy.Field()  #标题
    desc = scrapy.Field()
    tag = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    createtime = scrapy.Field()

    @property
    def module(self):
        return 'news'

class Process(Base):
    def process(self, item):
        sql = "INSERT INTO news (title, intro, tag, image, url, createtime) VALUES (%s, %s, %s, %s, %s, %s);"
        try:
            self.db.insert(sql, item['title'], item['desc'], item['tag'], item['image'], item['url'], item['createtime'])
        except Exception as e:
            print str(e)
        return item


class WwwToutiaoCom(scrapy.Spider):
    """
    scrapy crawl weixin
    抓取微信搜索首页内容
    """
    name = "www_toutiao_com"
    allowed_domains = ["toutiao.com" ]
    taglist = ['__all__', 'news_hot', 'news_society', 'news_entertainment', 'news_tech', 'news_car', 'news_fashion']
    start_urls = ['http://toutiao.com/api/article/recent/?count=100&category=%s&max_behot_time=%d' % (tag, int(time.time())-72000) for tag in taglist]

    def parse(self, response):
        logger.info('[%s] %s' % (datetime.date.today(), response.url))
        jsoncon = json.loads(response.body)
        if jsoncon['message'] == 'success':
            conlist = jsoncon['data']
            tag = {v.split('=')[0]: v.split('=')[1] for v in urlparse(response.url).query.split('&')}.get('category', '__all__')
            for con in conlist:
                if con['middle_mode']:
                    item = WwwToutiaoComItem()
                    item['title'] = con['title'].encode('utf-8')
                    item['tag'] = tag
                    item['desc'] = con['abstract'].encode('utf-8')
                    item['image'] = con['middle_image']
                    item['url'] = con['url']
                    item['createtime'] = con['create_time']
                    yield item
