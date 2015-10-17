# -*- coding: utf-8 -*-

import random
import base64

from scrapy.http import Request 
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from settings import USER_AGENTS

class ProxyError(Exception):
    pass

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        #动态从memcached中加载代理IP
        request.meta['proxy'] = None


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        #这句话用于随机选择user-agent
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))


class CheckProxyMiddleware(object):
    """检测代理的可用性"""
    def process_spider_input(self, response, spider):
        if response.status != 200:
            raise ProxyError
        else:
            return None

    def process_spider_exception(self, response, exception, spider):
        if exception == ProxyError:
            yield Request(url=response.url, callback=response.callback, meta=response.meta)
