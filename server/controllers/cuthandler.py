# -*- coding: utf-8 -*-

import tornado.gen
import tornado.web
import tornado.httpclient
import urllib

import utils

from basehandler import BaseHandler
from settings import BASEURL, searchserver

class Cut(BaseHandler):
    def initialize(self):
        super(Cut, self).initialize()
        self.method = self.request.method
        self.uri = searchserver + "cut/"
        self.body = None
        self.headers = self.request.headers

    @tornado.gen.coroutine
    def getCutFromGolang(self, text, mode):
        dict = {"text": text, "mode": mode}
        self.body = urllib.urlencode(dict)
        resp = yield self.client()
        raise tornado.gen.Return(resp)

    def get(self):
        return self.post()

    @utils.cache_error
    @utils.checkSign
    @tornado.gen.coroutine
    def post(self):
        text = self.get_argument("text", None)
        mode = self.get_argument("mode", None)
        if not text or not mode:
            self.write(utils.json_failed(401))
        response = yield self.getCutFromGolang(text, mode)
        self.write(response.body)
        print self.method
        print self.body
        print response.body
        self.finish()

