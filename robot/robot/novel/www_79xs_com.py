# -*- coding: utf-8 -*-
import json
from collections import defaultdict
import sys
import zlib
import time
import datetime

import scrapy
import torndb
from scrapy.http import Request 
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.exceptions import DropItem

from robot.const import BOY, GIRL, DEFAULT_INTRO
from robot.items import RobotItem
from robot.models.base import Base
import robot.utils

reload(sys)   
sys.setdefaultencoding('utf8') 


#抓取格式信息
class Www79xsComItem(RobotItem):
    title = scrapy.Field() #小说标题
    first = scrapy.Field() #一级分类
    second = scrapy.Field() #二级分类
    author = scrapy.Field()
    introduction = scrapy.Field() #简介
    picture = scrapy.Field()
    chapter = scrapy.Field() #章节
    subtitle = scrapy.Field() #副标题
    text = scrapy.Field() #小说正文
    novelsource = scrapy.Field() #小说简介页面
    contentsource = scrapy.Field() #原文地址

    @property
    def module(self):
        return 'novel'

#信息处理
class Process(Base):
    """novel models基础类"""
    def __init__(self):
        self.tag_list = self.loadTag()

    def loadTag(self):
        sql = "select * from tag"
        return self.db.query(sql)

    def reloadTag(self):
        return self.loadTag()

    def haveTag(self, first, second):
        """检测tag是否已经存在，如果存在返回True 否则返回False"""
        if (first, second) in [(v['first'], v['second']) for v in self.tag_list]:
            return True
        else:
            return False

    def updateTag(self, first, second):
        """将新tag更新到数据库，并重新加载, 赶回tag_list"""
        sql = "insert into tag (first, second, createtime) values (%d, '%s', curdate());" % (first, second)
        try:
            self.db.insert(sql)
        except Exception as e:
            print str(e)
        self.tag_list = self.reloadTag()
        return self.tag_list

    def insertFromItem(self, item):
        """将item插入到tag 和 content"""
        def get_tag_id(tag_name):
            """获取二级分类id"""
            for tag in self.tag_list:
                if tag['second'] == tag_name:
                    return tag['id']
            return None


        @robot.utils.checkHave
        def haveNovel():
            """检测Novel是否含有某个小说的简介链接，如果没有返回None"""
            sql = "select * from novel where novelsource='%s'" 
            return sql, self.db, [item['novelsource']]

        def insertNovel():
            """将item信息插入小说简介数据表"""
            second_tag = get_tag_id(item['second'])
            if second_tag:
                sql = """INSERT INTO novel (title, first, second, author, introduction, picture, novelsource, createtime) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s);"""
                result = self.db.insert(sql, item['title'], item['first'], second_tag, 
                        item['author'], item['introduction'], item['images'][0]['path'], item['novelsource'], datetime.date.today())
                return result

        @robot.utils.checkHave
        def haveContent():
            """检测小说详情页是否存在，如果没有返回None"""
            sql = "select * from content where contentsource='%s'"
            return sql, self.db, [item['contentsource']]

        def insertContent(novel):
            """将item插入小说内容数据表"""
            second_tag = get_tag_id(item['second'])
            if second_tag:
                sql = """insert into content (novelid, title, first, second, chapter, subtitle, text, contentsource, createtime) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s);""" 
                for k in ['title', 'first', 'chapter', 'subtitle', 'text', 'contentsource']:
                    if not dict(item).has_key(k):
                        return
                try:
                    self.db.insert(sql, novel, item['title'], item['first'], second_tag, item['chapter'], item['subtitle'], 
                            item['text'], item['contentsource'], datetime.date.today())
                except Exception as e:
                    print(str(e))


        #检测是否有新的tag        
        if not self.haveTag(item['first'], item['second']):
            self.updateTag(item['first'], item['second'])

        have_novel = haveNovel()
        have_content = haveContent()

        if not have_novel:
            print "insert:", item["title"], "and", item["title"]
            try:
                res = insertNovel()
            except Exception as e:
                print str(e)
            else:
                insertContent(res)
        elif have_novel and not have_content:
            print "have insert:", item["title"], "and insert:", item["subtitle"]
            insertContent(have_novel['id'])
        else:
            print "have insert:", item['title'], "and", item['subtitle']


    def process(self, item):
        self.insertFromItem(item)
        return item



#抓取
class Www79xsCom(scrapy.Spider):
    """蜘蛛抓取逻辑"""
    name = "www_79xs_com"
    allowed_domains = ["79xs.com"]
    start_urls = (
        'http://www.79xs.com/',
    )

    def __init__(self):
        self.girl_url = "/book/LC/165.aspx"

    def parse(self, response):
        """http://www.79xs.com 首页解析""" 
        print "首页：", response.url
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@id="navber"]/div[@class="subnav"]/ul/li/a/@href').extract()
        for site in sites:
            if site == self.girl_url:
                request = Request(url=urljoin_rfc(get_base_url(response), site), callback=self.urlListParse, meta={'first': GIRL})
            else:
                request = Request(url=urljoin_rfc(get_base_url(response), site), callback=self.urlListParse, meta={'first': BOY})
            yield request


    def urlListParse(self, response):
        """获取分类页面的url list，并解析"""
        print "分类页面首页：", response.url
        #获取最大页码参数
        def getArgument(url):
            large = 0
            v = url.split('?')[-1]
            #返回参数字典
            return dict(zip(*([iter([value for kv in v.split('&') for value in kv.split('=')])] * 2)))

        #获取url目录
        def getPath(url):
            return url.split('?')[0]

        hxs = scrapy.Selector(response)
        urls = hxs.select('//table[@id="_ctl0_pager"]/tr/td[@align="Right"]/a/@href').extract()
        if urls.__len__() == 0: 
            yield Request(url=response.url, callback=self.classParse, meta={'first': response.meta['first']})
        else: 
            url = urls[-1]
            page_info = getArgument(url)
            path = getPath(url)
            for url in [urljoin_rfc(get_base_url(response), path + '?tclassid=' + page_info['tclassid'] + '&page=' + str(u)) for u in range(1, int(page_info['page']) + 1)]:
                request = Request(url=url, callback=self.classParse, meta={'first': response.meta['first']})
                yield request


    def classParse(self, response):
        """分类页面解析"""
        print "分类页面:", response.url
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class="yl_nr_left"]/div[@class="yl_nr_lt2"]/ul')
        for site in sites:
            data = defaultdict(dict)
            data['title'] = site.xpath('li[@class="ynl3"]/a[2]/text()').extract()[0]
            author = site.xpath('li[@class="ynl6"]/a/text()').extract()
            if author.__len__() == 0:
                data['author'] = '无名'
            else:
                data['author'] = author[0]
            tag = site.xpath('li[@class="ynl2"]/a/text()').extract()[0]
            data['first'] = response.meta['first']
            data['second'] = tag
            url = site.xpath('li[@class="ynl3"]/a[2]/@href').extract()[0]
            request = Request(url=urljoin_rfc(get_base_url(response), url), callback=self.introParse, meta={'data': data})
            #print json.dumps(data, sort_keys=True, indent=4)
            yield request


    def introParse(self, response):
        """小说简介页面解析"""
        print "小说简介：", response.url
        hxs = scrapy.Selector(response)
        data = response.meta['data']
        intro = hxs.xpath('//div[@id="right"]/div[@id="info"]/p[2]/text()').extract()
        if intro.__len__() == 0:
            data['introduction'] = DEFAULT_INTRO
        else:
            data['introduction'] = intro[0]
        image = hxs.xpath('//div[@id="left"]/div[@class="fmian"]/div[@class="img"]/img/@src').extract()
        if image.__len__() == 0:
            data['image'] = None
        else:
            data['image_urls'] = [urljoin_rfc(get_base_url(response), image[0])]
        url = hxs.xpath('//div[@class="button"]/ul[@class="l"]/li[@class="b1"]/a/@href').extract()[0]
        data['novelsource'] = urljoin_rfc(get_base_url(response), url) 
        request = Request(url=data['novelsource'], callback=self.chapterPares, meta={'data': data})
        #print json.dumps(data, sort_keys=True, indent=4)
        yield request


    def chapterPares(self, response):
        """小说章节页面解析"""
        print "小说章节", response.url
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class="insert_list"]/dl/dd/ul/li')
        for i, site in enumerate(sites, 1):
            item = Www79xsComItem()
            for k, v in response.meta['data'].items():
                item[k] = v
            item['chapter'] = i
            subtitle = site.xpath('strong/a/text()').extract()
            if subtitle.__len__() != 0:
                item['subtitle'] = subtitle[0]
                item['contentsource'] = urljoin_rfc(get_base_url(response),site.xpath('strong/a/@href').extract()[0])
                request = Request(url=item['contentsource'], callback=self.contentPares, meta={'item': item})
                #print json.dumps(data, sort_keys=True, indent=4)
                yield request


    def contentPares(self, response):
        """小说内容页面解析"""
        print "小说内容", response.url
        hxs = scrapy.Selector(response)
        item = response.meta['item']
        sites = hxs.xpath('//div[@id="BookText"]/text()').extract()
        item['text'] = ('\n'.join(sites)).encode('utf-8')
        #print json.dumps(dict(item), sort_keys=True, indent=4)
        yield item
