# coding=utf-8

import time
import json
import re

import scrapy
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from robot.items import RobotItem

class WeixinSougouComItem(RobotItem):
    title = scrapy.Field()  #标题
    desc = scrapy.Field()
    cl = scrapy.Field()
    pic = scrapy.Field()
    url = scrapy.Field()
    largeimage = scrapy.Field()
    time = scrapy.Field()

class WeixinSougouCom(scrapy.Spider):
    """
    scrapy crawl weixin
    抓取微信搜索首页内容
    """
    name = "weixin_sougao_com"
    allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]
    start_urls = ["http://weixin.sogou.com/"]

    def parse(self, response):
        global cl
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@style="display:block"]/ul/li')
        for site in sites:
            title = site.select('div[@class="wx-news-info2"]/h4/a/text()').extract()[0][0:30]
            desc = site.select('div[@class="wx-news-info2"]/a/text()').extract()[0][0:200]
            pic = json.dumps(site.select('div[@class="wx-img-box"]/a/img/@src').extract())
            url = site.select('div[@class="wx-img-box"]/a/@href').extract()[0]
            if response.url == self.start_urls[0]:
                cl = 'weixin'
            t = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
            request = Request(url, callback=self.deepParse, meta={'title': title,
                                                                        'desc': desc,
                                                                        'pic': pic,
                                                                        'url': url,
                                                                        'cl': cl,
                                                                        'time': t, },)
            yield request

    def deepParse(self, response):
        item = WeisouItem()
        reg = r'var msg_cdn_url = "(.*?)";'
        rec = re.compile(reg, re.DOTALL)
        res = re.findall(rec, response.body)[0]
        item['title'] = response.meta['title']
        item['desc'] = response.meta['desc']
        item['pic'] = response.meta['pic']
        item['url'] = response.meta['url']
        item['cl'] = response.meta['cl']
        item['time'] = response.meta['time']
        item['largeimage'] = res
        item['image_urls'] = [res]
        yield item
