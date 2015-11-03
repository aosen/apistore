# -*- coding: utf-8 -*-

import sys
import datetime

import scrapy
from scrapy.http import Request 
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url

from robot.items import RobotItem
from robot.models.base import Base
from robot.settings import logger

reload(sys)   
sys.setdefaultencoding('utf8') 

#抓取格式信息
class BilibiliItem(RobotItem):
    title = scrapy.Field() #视频标题
    desc = scrapy.Field() #描述
    tag = scrapy.Field() #分类标签
    picurl = scrapy.Field() #缩略图
    videourl = scrapy.Field() #视频地址

    @property
    def module(self):
        return "player"

class Process(Base):
    """数据处理类"""

    def update(self, item):
        """数据更新"""
        def have():
            sql = "SELECT * FROM video WHERE video=%s"
            if not self.db.get(sql, item['videourl']):
                return False
            else:
                return True

        if not have():
            sql = "INSERT INTO video (title, intro, tag, image, video) VALUES (%s, %s, %s, %s, %s);"
            try:
                self.db.insert(sql, item['title'], item['desc'], item['tag'], item['picurl'],
                    item['videourl'])
            except Exception as e:
                print str(e)

    def process(self, item):
        self.update(item)
        return item

class Bilibiili(scrapy.Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    start_urls = (
        'http://www.bilibili.com/',
    )

    def parse(self, response):
        logger.info('[%s] %s' % (datetime.date.today(), response.url))
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class="menu-wrapper"]/ul/li[@class="m-i "]/a[@class="i-link"]')
        for s in sites:
            tag = s.xpath('em/text()').extract()[0]
            url = s.xpath('@href').extract()[0]
            request = Request(url=urljoin_rfc(get_base_url(response), url), callback=self.tagParse, meta={'tag': tag})
            yield request

    def tagParse(self, response):
        logger.info('[%s] %s' % (datetime.date.today(), response.url))
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class="b-body"]/ul[@class="vidbox v-list sub"]/li')
        tag = response.meta['tag']
        for s in sites:
            title = s.xpath('div/a/@title').extract()[0]
            desc = s.xpath('div/@txt').extract()[0]
            image = s.xpath('div/a/div/img/@src').extract()[0]
            url = s.xpath('div/a/@href').extract()[0]
            request = Request(url=urljoin_rfc(get_base_url(response), url), callback=self.videoParse, meta={"tag": tag, "title": title, "desc": desc, "image": image})
            yield request

    def videoParse(self, response):
        logger.info('[%s] %s' % (datetime.date.today(), response.url))
        hxs = scrapy.Selector(response)
        video = hxs.xpath('//meta[@itemprop="embedURL"]/@content').extract()[0]
        item = BilibiliItem()
        item['title'] = response.meta['title']
        item['desc'] = response.meta['desc']
        item['tag'] = response.meta['tag']
        item['picurl'] = response.meta['image']
        item['videourl'] = video
        yield item
