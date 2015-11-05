# -*- coding: utf-8 -*-

import json

import tornado.gen
import tornado.web
import tornado.httpclient

import utils
from basehandler import BaseHandler

class Index(BaseHandler):
    def get(self):
        self.write("hello world")