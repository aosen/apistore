# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpclient
import tornado.gen

from models.basemodel import PoolDB


class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.appid = self.get_argument("appid", None)

    def on_finish(self):
        if not self._finished:
            self.finish()

    @tornado.gen.coroutine
    def client(self):
        req = tornado.httpclient.HTTPRequest(
            self.uri,
            method=self.method,
            body=self.body,
            headers=self.headers,
            follow_redirects=False,
            allow_nonstandard_methods=True)
        client = tornado.httpclient.AsyncHTTPClient()
        resp = yield client.fetch(req)
        raise tornado.gen.Return(resp)