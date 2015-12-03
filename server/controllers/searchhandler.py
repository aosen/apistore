# -*- coding: utf-8 -*-

import json
import urllib

import tornado.gen
import tornado.web
import tornado.httpclient

import utils
import const
from basehandler import BaseHandler
from models.searchmodel import SearchModel
from settings import searchserver

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Search(BaseHandler):
    """
    搜索工厂类
    """

    def __init__(self, application, request, **kwargs):
        super(Search, self).__init__(application, request, **kwargs)

    def initialize(self):
        self.fd = SearchModel()

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
        super(IndexAction, self).initialize()
        self.uri = searchserver+"index/"
        self.body = self.request.body
        self.headers = self.request.headers
        self.response = None
        self.text = None
        self.docid = None
        self.tags = None

    @tornado.gen.coroutine
    @utils.cache_error
    def index(self):
        self.docid = str(utils.encodeDocid(int(self.appid), int(self.docid)))
        data = {"docid": self.docid}
        if self.tags:
            data["tags"] = self.tags
        if self.text:
            data["text"] = self.text
        self.body = urllib.urlencode(data)
        resp = yield self.client()
        raise tornado.gen.Return(resp)

    @utils.cache_error
    @utils.checkSign
    @tornado.gen.coroutine
    def post(self):
        self.appid = self.get_argument("appid", None)
        self.text = self.get_argument("text", None)
        self.docid = self.get_argument("docid", None)
        self.tags = self.get_argument("tags", None)
        #检测text tags的长度
        if self.text and len(self.text) > const.MAX_TEXT_TAGS or self.tags and len(self.tags) > const.MAX_TEXT_TAGS:
            self.write(utils.json_failed(401))
        if not self.text or int(self.docid) < 1 or int(self.docid) > const.MAX_DOCID:
            self.write(utils.json_failed(401))
        else:
            self.response = yield self.index()
            self.write(self.response.body)

    def on_finish(self):
        """
        信息返回给用户后接下来的操作都在这里
        :return: 无
        """
        # 如果搜索引擎返回code=200, 则将索引信息加入mysql
        if self.response and json.loads(self.response.body)["code"] == 200:
            self.fd.addIndex(self.appid, self.docid)
        super(IndexAction, self).on_finish()


class SearchAction(Search):
    def __init__(self, application, request, **kwargs):
        super(SearchAction, self).__init__(application, request, **kwargs)
        self.appid = self.get_argument("appid", None)

    def initialize(self):
        super(SearchAction, self).initialize()
        self.uri = searchserver+"search/?"
        self.body = self.request.body
        self.headers = self.request.headers

    @tornado.gen.coroutine
    def search(self):
        """
        text / tags / docids (text与tags至少有一项不为空,docids为必填项) / timeout (可选)
        :type docids: string
        return: 返回错误编码或respone
        """
        if not self.appid:
            raise tornado.gen.Return(401)
        if not self.text and not self.tags:
            raise tornado.gen.Return(401)
        if not self.docids:
            raise tornado.gen.Return(401)
        # 还原docids
        docidslist = self.docids.split("-")
        if len(docidslist) != 2:
            raise tornado.gen.Return(401)
        else:
            docidslist[0] = str(utils.encodeDocid(int(self.appid), int(docidslist[0])))
            docidslist[1] = str(utils.encodeDocid(int(self.appid), int(docidslist[1])))
        self.uri = self.uri + "docids=" + docidslist[0] + "-" + docidslist[1]
        if self.text:
            self.uri = self.uri + "&text=" + self.text
        if self.tags:
            self.uri = self.uri + "&tags=" + self.tags
        if self.timeout:
            self.uri = self.uri + "&timeout=" + self.timeout
        resp = yield self.client()
        raise tornado.gen.Return(resp)

    @utils.cache_error
    @utils.checkSign
    @tornado.gen.coroutine
    def post(self):
        self.text = self.get_argument("text", None)
        self.docids = self.get_argument("docids", None)
        self.tags = self.get_argument("tags", None)
        self.timeout = self.get_argument("timeout", None)
        self.response = yield self.search()
        if self.response == 401:
            self.write(utils.json_failed(401))
        else:
            tmp = json.loads(self.response.body)["result"]
            r = {}
            r["tokens"] = tmp["Tokens"]
            r["docs"] = [utils.decodeDocid(int(self.appid), int(docid['DocId'])) for docid in tmp["Docs"]]
            r["timeout"] = tmp["Timeout"]
            self.write(utils.json_success(r))
        self.finish()
