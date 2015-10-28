# -*- coding: utf-8 -*-

import json
import time

from tornado.web import RequestHandler
import tornado.httpclient
import tornado.gen

import utils
import const
from models.newsbase import NewsBase

class news(RequestHandler):
    """news的基类"""
    news = NewsBase()

class GetSinaGirl(news):
    """获取新浪女孩的列表"""
    l = [
        # 视觉大片
        'photograph_gallery',
        # 八卦
        'gossip',
        # 服饰搭配
        'style',
        # 美体瘦身
        'body',
        # 彩妆美发
        'beauty',
    ]

    def get(self):
        return self.post()

    @utils.cache_error
    #@utils.checkSign
    def post(self):
        tag = self.get_argument("tag", None)
        tag = tag if tag in self.l else None
        page = self.get_argument("page", None)
        page = 1 if not page else int(page)
        limit = self.get_argument("limit", None)
        limit = const.NEWS_LIMIT if not limit else int(limit)
        pic_list = self.news.loadSinaGirlPic(tag, page, limit) 
        result = [{'title': v['title'], 'tag': v['cl'], 'picon': json.loads(v['picmsg']), 'time': v['createtime']} for v in pic_list]
        self.write(utils.json_success(result))


class GetNews(news):
    """获取新闻列表加置顶信息"""
    l = [
            #推荐
            '__all__',
            #热门
            'news_hot',
            #社会
            'news_society',
            #娱乐
            'news_entertainment',
            #科技
            'news_tech',
            #汽车
            'news_car',
            #时尚
            'news_fashion',
            ]

    def get(self):
        return self.post()

    @utils.cache_error
    #@utils.checkSign
    def post(self):
        tag = self.get_argument('tag', None)
        tag = tag if tag in self.l else '__all__'
        page = self.get_argument("page", None)
        page = 1 if not page else int(page)
        limit = self.get_argument("limit", None)
        limit = const.NEWS_LIMIT if not limit else int(limit)
        print page, limit, tag
        news_list = self.news.loadNews(tag, page, limit) 
        print news_list
        result = [{'title': v['title'], 'image': v['image'], 'desc': v['intro'], 'url': v['url'], 'create_time': v['createtime']} for v in news_list]
        self.write(utils.json_success(result))
