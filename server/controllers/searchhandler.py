# -*- coding: utf-8 -*-

import json

import tornado.gen
import tornado.web
import tornado.httpclient

import utils

#docids的范围 1-999999999999
DOCIDSIZE = 1000000000000

class Search(tornado.web.RequestHandler):
    def initialize(self):
        self.uri = "http://127.0.0.1:2019/search/"
        self.body = self.request.body
        self.headers = self.request.headers

    def search(self, text, docids, tags, timeout):
        """
        :type docids: string
        """

        def decode_docids():
            """
            :rtype: string
            """
            l = []
            docidl = docids.split("-")
            assert isinstance(docidl, list)
            for id in range(docidl):
                pass


        if docids:
            decode_docids()

    def get(self):
        return self.post()

    @tornado.gen.coroutine
    def post(self):
        text = self.get_argument("text", None)
        docids = self.get_argument("docids", None)
        tags = self.get_argument("tags", None)
        timeout = self.get_argument("timeout", None)
        self.search(text, docids, tags, timeout)
        self.write("hello world")
        self.finish()