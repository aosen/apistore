# -*- coding: utf-8 -*-

import json
import datetime
import hashlib
import traceback

import tornado.gen

from models.base import Base
from settings import logger
from const import MAX_DOCID

errcode = {
    401: "参数不正确",
    402: "验证失败",
    403: "缺少sign_method参数",
    404: "缺少sign参数",
    405: "非法用户",
    406: "不存在",
    500: "未知错误",
    #业务层面的错误
    601: "用户名已经存在",
}


def json_success(result):
    data = {"code": 200, "desc": "success", "result": result}
    return json.dumps(data, cls=JsonEncoder)


def json_failed(code, err=None):
    if code == 500:
        data = {"code": code, "desc": str(err), "result": "{0}".format(traceback.format_exc())}
    else:
        data = {"code": code, "desc": errcode[code], "result": "{0}".format(str(err))}
    return json.dumps(data, cls=JsonEncoder)


def cache_error(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            code = e.args[0]
            if isinstance(code, int) and code in errcode:
                self.write(json_failed(code))
            else:
                self.write(json_failed(500, err=e))

    return wrapper

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def checkSign(func):
    """验证开发者发过来的sign，进行web api访问权限判断"""

    def wrapper(*args, **kwargs):
        self = args[0]
        sign = self.get_argument('sign', None)
        if not sign:
            raise ValueError(404)
        appid = self.get_argument('appid', None)
        if not appid:
            raise ValueError(405)

        model_base = Base()
        arguments = sorted(self.request.arguments.iteritems(), key=lambda x: x[0])
        result_string = ''.join([k + v[0] for k, v in arguments if k != 'sign'])
        appsecret = model_base.getAppSercet(appid)
        if not appsecret:
            raise ValueError(405)

        def default(*args):
            raise ValueError(403)

        def md5Method(result_string, appsecret):
            return hashlib.md5(appsecret + result_string + appsecret).hexdigest()

        switch = {
            'md5': md5Method,
        }

        mysign = switch.get(self.get_argument('sign_method', None), default)(result_string, appsecret)
        logger.info("sign:%s" % mysign)
        if mysign != sign:
            raise ValueError(402)
        return func(*args, **kwargs)

    return wrapper


def encodeDocid(appid, docid):
    """
    编码docid 算法: appid*MAX_DOCID + docid
    :param docid:
    :return: new_docid
    """
    return appid * MAX_DOCID + docid


def decodeDocid(appid, docid):
    """
    解码docid 算法: newdocid = docid - appid * MAX_DOCID
    :param appid:
    :param docid:
    :return: new_docid
    """
    return docid - appid * MAX_DOCID

def encodePassword(password):
    """
    密码加密策略,采用sha1加密
    :param password: 原始密码
    :return: 加密后密码
    """
    return hashlib.sha1(password).hexdigest()