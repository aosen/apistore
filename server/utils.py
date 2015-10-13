# -*- coding: utf-8 -*-

import json
import datetime
import hashlib
import traceback

from models.base import Base
from settings import logger

errcode = {
        1: "参数不正确",
        2: "验证失败", 
        3: "缺少sign_method参数",
        4: "缺少sign参数",
        5: "非法用户",
        500: "未知错误",
        }


def json_success(result):
    data = {"err": 0, "errmsg": "", "result": result}
    return json.dumps(data, cls=JsonEncoder)


def json_failed(code, err=None):
    if code == 500:
        data = {"err": code, "errmsg": str(err), "result": "{0}".format(traceback.format_exc())}
    else:
        data = {"err": code, "errmsg": errcode[code], "result": "{0}".format(str(err))}
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
            raise ValueError(4)
        appid = self.get_argument('appid', None)
        if not appid:
            raise ValueError(5)

        model_base = Base()
        arguments = sorted(self.request.arguments.iteritems(), key=lambda x: x[0])
        result_string = ''.join([k+v[0] for k, v in arguments if k != 'sign'])
        appsecret = model_base.getAppSercet(appid)
        if not appsecret:
            raise ValueError(5)

        def default(*args):
            raise ValueError(3)

        def md5Method(result_string, appsecret):
            return hashlib.md5(appsecret + result_string + appsecret).hexdigest()

        switch = {
                'md5': md5Method,
                }

        mysign = switch.get(self.get_argument('sign_method', None), default)(result_string, appsecret)
        logger.info("sign:%s" % mysign)
        if mysign != sign:
            raise ValueError(2)
        return func(*args, **kwargs)
    return wrapper

