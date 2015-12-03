# -*- coding: utf-8 -*-

"""
IM web api
"""

from models.immodel import ImModel


class Im(BaseHandler):
    """
    Im 工厂类
    """
    def initialize(self):
        self.fd = ImModel()
        self.token = None
        self.getTokenUrl = "https://api.gotye.com.cn/api/accessToken"

    def getToken(self):
        if self.token == None or self.token.hasExpires():
            param = json.dumps(param)
            print "url: -- ",self.baseUrl
            print "req: -- ",param
            request = urllib2.Request(self.baseUrl+"/accessToken",data=param)
            request.add_header('Content-Type', 'application/json')
            resp_data = urllib2.urlopen(request)
            resp_str = resp_data.read()
            print "resp: -- ",resp_str
            res = json.loads(resp_str)
            self.token = Token(res["access_token"],res["expires_in"])
            if "api_url" in res :
                self.baseUrl = res["api_url"]
        return self.token