# coding=utf-8

import json
import time

import scrapy

from robot.items import RobotItem

class WwwToutiaoComItem(RobotItem):
    title = scrapy.Field()  #标题
    desc = scrapy.Field()
    cl = scrapy.Field()
    pic = scrapy.Field()
    url = scrapy.Field()
    largeimage = scrapy.Field()
    time = scrapy.Field()


class WwwToutiaoCom(scrapy.Spider):
    """
    scrapy crawl weixin
    抓取微信搜索首页内容
    """
    name = "www_toutiao_com"
    allowed_domains = ["http://toutiao.com/"]
    start_urls = ['http://toutiao.com/api/article/recent/']

    def parse(self, response):
        jsoncon = json.loads(response.body)
        if jsoncon['message'] == 'success':
            conlist = jsoncon['data']
            for con in conlist:
                item = WwwToutiaoComItem()
                item['title'] = con['title']
                item['cl'] = con['tag']
                item['desc'] = con['abstract']
                item['image_urls'] = []
                l = []
                for pic in con['image_list']:
                    l.append(pic['url'])
                item['pic'] = json.dumps(l)
                item['url'] = con['url']
                item['time'] = time.strftime("%Y-%m-%d", time.localtime(int(con['create_time'])))
                if con.has_key('large_image_url'):
                    item['largeimage'] = con['large_image_url']
                else:
                    if len(con['image_list']):
                        item['largeimage'] = con['image_list'][0]['url']
                    else:
                        item['largeimage'] = ''
                yield item
        else:
            print 'fail'
