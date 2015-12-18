# -*- coding: utf-8 -*-

import os
import socket
import logging

DEBUG = True

#base url
BASEURL = "http://127.0.0.1:8000"

#数据库信息
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'aosencloud',  # Or path to database file if using sqlite3.
    'USER': 'root',  # Not used with sqlite3.
    'PASSWORD': 'zhangzhen',  # Not used with sqlite3.
    'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '3307',  # Set to empty string for default. Not used with sqlite3.
    'MAXCONN': 1, #连接池容量
    }
}
MEMCACHE = {
        'ADDR': '127.0.0.1:11211',
        }

logger = logging.getLogger('apistore')

#scrapy图片下载路径
IMAGES_STORE = '/Users/zhangzhen/apistore/static/spider/'

#search连接配置
searchserver = "http://127.0.0.1:2019/"

#模板目录
TEMPLATE_PATH = "/home/zhen/apistore/template/"
#静态文件目录
STATIC_PATH = "/home/zhen/apistore/static/"

#web api 账户密码
appid = "10000"
appsecret = "c174cb1fda3491285be953998bb867a0"

SECRET_KEY = '8ch#eyg(h-fio1!-dok5k)4hy5&8(=ztr$==(i87a(^i#ut8*d'

GOTYE_APPKEY = '69a3b835-9f08-478b-b3fd-18cf36e5594e'
