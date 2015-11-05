# -*- coding: utf-8 -*-

import json

import tornado.gen
import tornado.web
import tornado.httpclient

import utils
import const
from basehandler import BaseHandler
from models.searchbase import SearchBase

class Search(BaseHandler):
    """
    搜索工厂类
    """
    fd = SearchBase()

    @tornado.gen.coroutine
    def client(self):
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

class IndexAction(Search):
    def initialize(self):
        self.uri = "http://127.0.0.1:2019/index/"
        self.body = self.request.body
        self.headers = self.request.headers

    @tornado.gen.coroutine
    def index(self, text, docid, tags):
        if tags:
            self.uri = self.uri+"?text="+text+"&docid="+docid+"&tags="+tags
        else:
            self.uri = self.uri+"?text="+text+"&docid="+docid
        resp = yield self.client()
        raise tornado.gen.Return(resp)

    @utils.cache_error
    #@utils.checkSign
    @tornado.gen.coroutine
    def post(self):
        text = self.get_argument("text", None)
        docid = self.get_argument("docid", None)
        tags = self.get_argument("tags", None)
        if not text or int(docid) < 1 or int(docid) > const.MAX_DOCID:
            raise ValueError(1)
        else:
            try:
                response = yield self.index(text, docid, tags)
            except Exception as e:
                raise ValueError(500)
            else:
                #如果搜索引擎返回err=0, 则将索引信息加入mysql
                data = json.loads(response.body)
                if json.loads(response.body)["err"] == 0:
                    self.fd.addIndex(self.appid, docid)
                self.write(response.body)
        self.finish()

class SearchAction(Search):
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

    @tornado.gen.coroutine
    def post(self):
        text = self.get_argument("text", None)
        docids = self.get_argument("docids", None)
        tags = self.get_argument("tags", None)
        timeout = self.get_argument("timeout", None)
        self.search(text, docids, tags, timeout)
        self.write("hello world")
        self.finish()