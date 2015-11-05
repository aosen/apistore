# -*- coding: utf-8 -*-

import tornado.gen
import tornado.web
import tornado.httpclient


class BaseHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def prepare(self):
        self.appid = self.get_argument("appid", None)
