# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
小说内容索引脚本,基于gevent
"""

import urllib2
import urllib
import logging
import hashlib
import json
import Queue
import signal

import gevent

import sys
sys.path.append("../")
reload(sys)
sys.setdefaultencoding('utf8')
from settings import DATABASES, logger, appid, appsecret, BASEURL

import torndb

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
    fh = logging.FileHandler('novelindex.log')
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

class Model(object):
    """models类"""

    @property
    def db(self):
        #此处后期需要改为连接池,将数据库连接放在启动服务器的时候
        return torndb.Connection(
                DATABASES['HOST']+':'+DATABASES['PORT'],
                DATABASES['NAME'],
                user=DATABASES['USER'],
                password=DATABASES['PASSWORD']
                )

    #一次性将数据全部读出,然后进行迭代, 反正目前也就3000千条数据
    def loadAllData(self):
        """返回小说简介的所有行"""
        sql = "SELECT id, title, second, author, introduction FROM novel"
        return self.db.query(sql)

    def loadSecond(self):
        """获取二级分类字典"""
        sql = "SELECT id, second FROM tag"
        return self.db.query(sql)

class RpcClientManage(object):
    """rpc客户端管理器, 控制产生客户端的个数"""

    def __init__(self, clientNum):
        self.clientNum = clientNum
        self.clientPoll = self._clientPoll()

    def _clientPoll(self):
        clients = Queue.Queue(maxsize = clientNum)
        for i in range(self.clientNum):
            clients.put(RpcClient(self))
        return clients

    def client(self):
        return self.clientPoll.get()

    def close(self, rpcclient):
        self.clientPoll.put(rpcclient)


class RpcClient(object):
    """rpc client 与Golang的搜索引擎服务器进行通信"""

    def __init__(self, manage):
        self.indexurl = BASEURL + "/index/"
        self.appid = appid
        self.appsecret = appsecret
        self.manage = manage

    def post(self, url, body):
        """post提交和获取搜索引擎服务器内容"""
        req = urllib2.Request(url)
        body = urllib.urlencode(body)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, body)
        return response.read()

    @cache_error
    def index(self, text, docid, tags):
        """
        建立索引
        如果建立索引返回True
        """
        if not text and not tags or not docid:
            raise ValueError(401)
        body = {"docid": docid, "appid": appid, "sign_method": "md5"}
        if text:
            body["text"] = text
        if tags:
            body["tags"] = tags
        body["sign"] = md5sign(appsecret, body)
        res = self.post(self.indexurl, body)
        result = json.loads(res)
        resultcode = result["code"]
        if resultcode != 200:
            logger.error(result["desc"])
        else:
            logger.debug(result)
        self.manage.close(self)

if __name__ == "__main__":
    #初始化日志
    initLog(logging.DEBUG)
    #将数据库内容一条条的发送给搜索引擎服务器建立索引
    fd = Model()
    datalist = fd.loadAllData()
    secondlist = fd.loadSecond()
    #生成分类字典
    tagdict = {}
    for second in secondlist:
        tagdict[second["id"]] = second["second"]
    #生成20个线程
    clientNum = 100
    clientPoll = RpcClientManage(clientNum)
    gevent.signal(signal.SIGQUIT, gevent.kill)
    for data in datalist:
        text = data["title"] + data["introduction"] + tagdict[data["second"]] + data["author"]
        docid = data["id"]
        thread = gevent.spawn(clientPoll.client().index, text, docid, None)
        thread.join()