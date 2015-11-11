# -*- coding: utf-8 -*-

"""
IM web api
"""

import time
import json
import urllib2

from basehandler import BaseHandler
from models.gotyebase import GotyeBase
import utils

class Token(object):
    """Token类 获取Token与验证Token是否超时"""

    token = None
    expires_in = 0
    expires_in_sec = time.time() + expires_in
    param = {
        "grant_type": "client_credentials",
        "client_id": "8260709d-549e-4bd9-99db-bceff58da787",
        "client_secret": "ef52b408d24a4535bc30c2916a822353",
    }
    getTokenUrl = "https://api.gotye.com.cn/api/accessToken"
    apiUrl = None

    @classmethod
    def hasExpires(cls):
        return self.expires_in_sec <= time.time()

    @classmethod
    def getToken(cls):
        if cls.token == None or cls.hasExpires():
            param = json.dumps(cls.param)
            print "url: -- ", cls.getTokenUrl
            print "req: -- ", cls.param
            request = urllib2.Request(cls.getTokenUrl, data=param)
            request.add_header('Content-Type', 'application/json')
            resp_data = urllib2.urlopen(request)
            resp_str = resp_data.read()
            print "resp: -- ", resp_str
            res = json.loads(resp_str)
            cls.token = res["access_token"]
            cls.expires_in = res["expires_in"]
            if "api_url" in res:
                cls.apiUrl = res["api_url"]
        return cls.token


class Gotye(BaseHandler):
    """
    Im 工厂类
    """
    def initialize(self):
        self.fd = GotyeBase()

class GotyeToken(Gotye):
    """获取im token信息"""

    @utils.cache_error
    #@utils.checkSign
    def get(self):
        self.write(Token.getToken())