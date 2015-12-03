# -*- coding: utf-8 -*-

import json
import tornado.gen
import tornado.web

import utils
from basehandler import BaseHandler
from models.userauthmodel import UserAuthModel

class UserAuth(BaseHandler):
    """用户验证工厂类"""
    def __init__(self, application, request, **kwargs):
        super(UserAuth, self).__init__(application, request, **kwargs)

    def initialize(self):
        self.fd = UserAuthModel()

def check_register_arg(func):
    def wrapper(*args, **kwargs):
        """
        验证用户名和密码的合法性
        :param args: self = args[0]
        :param kwargs:
        :return: 如果验证成功返回True 失败返回False
        """
        self = args[0]
        self.username = self.get_argument("username", None)
        self.password = self.get_argument("password", None)
        if not self.username or not self.password:
            self.write(utils.json_failed(401))
        else:
            return func(*args, **kwargs)
    return wrapper

class RegisterAction(UserAuth):
    """处理用户注册行为"""
    """2015-11-25 后期需要增加图片验证码"""
    
    def initialize(self):
        super(RegisterAction, self).initialize()
        self.username = None
        self.password = None

    def get(self):
        return self.post()

    @utils.cache_error
    #@utils.checkSign
    @check_register_arg
    def post(self):
        #如果username 和 password 合法,则访问数据库,如果appid下的username已经存在,则返回601
        if self.fd.haveUserName(self.appid, self.username):
            self.write(utils.json_failed(601))
        else:
            if not self.fd.saveUserInfo(self.appid, self.username, self.password):
                self.write(utils.json_failed(500))
            else:
                self.write(utils.json_success("注册成功"))

class LoginAcion(UserAuth):
    """处理用户登录行为"""
    pass