# -*- coding: utf-8 -*-

import json

import tornado.gen
import tornado.web
import tornado.httpclient

import utils

class Cut(tornado.web.RequestHandler):
    def initialize(self):
        self.uri = "http://127.0.0.1:2019/"
        self.body = self.request.body
        self.headers = self.request.headers

    @tornado.gen.coroutine
    def getCutFromGolang(self, text, mode):
        if text and mode:
            self.uri = self.uri+"?text="+text+"&mode="+mode
        req = tornado.httpclient.HTTPRequest(
                self.uri, 
                method=self.request.method, 
                body=self.body, 
                headers=self.headers, 
                follow_redirects=False, 
                allow_nonstandard_methods=True)
        client = tornado.httpclient.AsyncHTTPClient()
        resp = yield client.fetch(req)
        raise tornado.gen.Return(resp)

    def get(self):
        return self.post()

    @utils.cache_error
    @utils.checkSign
    @tornado.gen.coroutine
    def post(self):
        text = self.get_argument("text", None)
        mode = self.get_argument("mode", None)
        response = yield self.getCutFromGolang(text, mode)
        self.write(response.body) 
        self.finish()

