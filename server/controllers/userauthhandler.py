# -*- coding: utf-8 -*-

import json
import tornado.gen
import tornado.web

import utils
from basehandler import BaseHandler
from models.userauthmodel import UserAuthModel

from settings import GOTYE_APPKEY, logger

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

class CheckUser(UserAuth):
    """处理亲加用户登录行为"""

    @utils.cache_error
    def get(self):
        """验证亲加通信云的用户认证信息"""
        def fail(account):
            self.write(json.dumps({"status": "error", "account": account, "appkey": GOTYE_APPKEY}))
        def checkSign(**kwargs):
            """验证签名"""
            arguments = sorted(kwargs.iteritems(), key=lambda x: x[0])
            result_string = ''.join([k + v[0] for k, v in arguments if k != 'sign'])
            appsecret = self.fd.getAppSercet(kwargs['appid'])
            if not appsecret:
                return False
            else:
                def md5Method(result_string, appsecret):
                    return hashlib.md5(appsecret + result_string + appsecret).hexdigest()

                def default(*args):
                    return ""

                switch = {
                    'md5': md5Method,
                }

                mysign = switch.get(kwargs["sign_method"], default)(result_string, appsecret)
                logger.info("sign:%s" % mysign)
                if mysign != sign:
                    return False
                else:
                    return True
        appkey = self.get_argument("appkey", None)
        account_sign = self.get_argument("account", None)
        password = self.get_argument("password", None)
        #account_appid_method_sign
        if appkey != GOTYE_APPKEY or not account_sign or not password:
            fail(account_sign)
        else:
            res = account_sign.split("_")
            if len(res) != 4:
                fail(account_sign)
            else:
                account, appid, method, sign = res
                if not checkSign(account=account, appid=appid, method=method, sign=sign):
                    fail(account_sign)
                else:
                    if self.fd.checkUserInfo(appid, account, password):
                        self.write(json.dumps({"status": "ok", "account": account, "appkey":GOTYE_APPKEY}))
                    else:
                        fail(account_sign)