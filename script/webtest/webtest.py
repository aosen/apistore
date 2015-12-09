# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
网站测试脚本
"""

import urllib2
import urllib
import logging
import hashlib
import json
import Queue
import signal
import copy
import time

import gevent

import sys
sys.path.append("../")
reload(sys)
sys.setdefaultencoding('utf8')
from settings import DATABASES, logger, appid, appsecret, BASEURL

import torndb

from const import testurl, baseurl

errcode = {
    401: "参数不正确",
    402: "验证失败",
    403: "缺少sign_method参数",
    404: "缺少sign参数",
    405: "非法用户",
    406: "不存在",
    500: "未知错误",
    #业务层面的错误
    601: "用户名已经存在",
}


def initLog(level):
    """初始化日志"""
    logger.setLevel(level)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('webtest.log')
    fh.setLevel(level)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # 定义handler的输出格式
    formatter = logging.Formatter('[%(asctime)s-%(name)s-%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)


def cache_error(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if len(e.args) > 1:
                code = e.args[0]
            else:
                code = None
            if isinstance(code, int) and code in errcode:
                logger.error(str(code)+" "+errcode[code]+" "+str(args))
            else:
                logger.error("500"+" "+str(e)+" "+str(args))

    return wrapper

def md5sign(appsecret, dict):
    """生成签名"""
    #字典排序
    dictsort = sorted(dict.iteritems(), key = lambda asd:asd[0])
    #字符串拼装
    sortstr = "".join([str(v) for value in dictsort for v in value])
    return hashlib.md5(appsecret + sortstr + appsecret).hexdigest()

class ClientManage(object):
    """rpc客户端管理器, 控制产生客户端的个数"""

    def __init__(self, clientNum):
        self.clientNum = clientNum
        self.clientPoll = self._clientPoll()

    def _clientPoll(self):
        clients = Queue.Queue(maxsize = clientNum)
        for i in range(self.clientNum):
            clients.put(Client(self))
        return clients

    def client(self):
        return self.clientPoll.get()

    def close(self, client):
        self.clientPoll.put(client)


class Client(object):
    """rpc client 与Golang的搜索引擎服务器进行通信"""

    def __init__(self, manage):
        self.manage = manage

    @cache_error
    def post(self, url, body):
        """post提交和获取搜索引擎服务器内容"""
        req = urllib2.Request(url)
        body = urllib.urlencode(body)
        #enable cookie
        t1 = time.time()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, body)
        r = response.read()
        t2 = time.time()
        logger.info("time:" + str(t2-t1) + " " +url+"?"+ body + " code:" + str(json.loads(r)['code']))
        self.manage.close(self)

if __name__ == "__main__":
    #初始化日志
    initLog(logging.DEBUG)
    #生成500个线程
    clientNum = 100
    clientPoll = ClientManage(clientNum)
    gevent.signal(signal.SIGQUIT, gevent.kill)
    loop = 1
    i = 0
    l = len(testurl)
    timedict = {}
    for item in testurl:
        timedict[item['url']] = []
    for _ in range(loop):
        for item in testurl:
        #while True:
            t1 = time.time()
            url = baseurl + testurl[i%l]['url']
            if testurl[i%l].has_key('body'):
                dict = copy.deepcopy(testurl[i%l]['body'])
            else:
                dict = {}
            dict['appid'] = appid
            dict['sign_method'] = "md5"
            dict['sign'] = md5sign(appsecret, dict)
            thread = gevent.spawn(clientPoll.client().post, url, dict)
            thread.join(1)
            i += 1
            t2 = time.time()
            timedict[item['url']].append(t2-t1)
    average = {}
    for k, v in timedict.items():
        average[k] = sum(v) / loop
    print average