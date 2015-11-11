# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpclient


class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.appid = self.get_argument("appid", None)

    def on_finish(self):
        if not self._finished:
            self.finish()