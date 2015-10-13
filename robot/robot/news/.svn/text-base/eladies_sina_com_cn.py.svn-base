# -*- coding: utf-8 -*-
import sys
import time
import json
import datetime

import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import robot
from robot.items import RobotItem
from robot.models.base import Base

class EladiedSinaComCnItem(RobotItem):
    title = scrapy.Field()  #标题
    cl = scrapy.Field()     #分类
    picmsg = scrapy.Field() #图片信息
    time = scrapy.Field()   #创建时间

    @property
    def module(self):
        return 'news'


class Process(Base):
    def __init__(self):
        pass

    def process(self, item):

        @robot.utils.checkHave
        def havePicGirl():
            """检测是否存在条目"""
            sql = """SELECT * FROM girlpic WHERE picmsg=%s"""
            return sql, self.db, [item['picmsg']]

        if not havePicGirl():
            sql = """INSERT INTO girlpic (title, cl, picmsg, createtime) values (%s, %s, %s, %s)"""
            self.db.insert(sql, item['title'], item['cl'], item['picmsg'], datetime.date.today())


class EladiedSinaComCn(scrapy.Spider):
    """
    抓取微信搜索首页内容
    """
    name = "eladies_sina_com_cn"
    allowed_domains = ["sina.com.cn", ]
    start_urls = ["http://eladies.sina.com.cn/photo/", ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        l = [
            # 视觉大片
            {'id': 'SI_Scroll_2_Cont', 'cl': 'photograph_gallery'},
            # 八卦
            {'id': 'SI_Scroll_3_Cont', 'cl': 'gossip'},
            # 服饰搭配
            {'id': 'SI_Scroll_4_Cont', 'cl': 'style'},
            # 美体瘦身
            {'id': 'SI_Scroll_5_Cont', 'cl': 'body'},
            # 彩妆美发
            {'id': 'SI_Scroll_6_Cont', 'cl': 'beauty'},
        ]
        for d in l:
            sites = hxs.select('//div[@id="%s"]/div/div/a/@href' % d['id']).extract()
            for site in sites:
                cl = d['cl']
                request = Request(site, callback=self.deepParse, meta={'cl': cl},)
                yield request

    def deepParse(self, response):
        hxs = HtmlXPathSelector(response)
        item = EladiedSinaComCnItem()
        item['title'] = hxs.select('//div[@id="eData"]/dl[1]/dt/text()').extract()[0]
        picl = hxs.select('//div[@id="eData"]/dl/dd[1]/text()').extract()
        descl = hxs.select('//div[@id="eData"]/dl/dd[5]/text()').extract()
        item['time'] = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        item['cl'] = response.meta['cl']
        item['picmsg'] = json.dumps([{'pic': pic, 'desc': desc} for (pic, desc) in zip(picl, descl)])
        yield item
