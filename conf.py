# -*- coding: utf-8 -*-

import os
import socket

#数据库信息
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'aosencloud',  # Or path to database file if using sqlite3.
            'USER': 'root',  # Not used with sqlite3.
            'PASSWORD': 'zhangzhen',  # Not used with sqlite3.
            'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3307',  # Set to empty string for default. Not used with sqlite3.
            },
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'aosencloud',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': 'zhangzhen',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3307',  # Set to empty string for default. Not used with sqlite3.
        }
MEMCACHE = {
        'ADDR': '127.0.0.1:11211',
        }

#scrapy图片下载路径
IMAGES_STORE = '/Users/zhangzhen/apistore/static/spider/'

#search连接配置
searchserver = "http://127.0.0.1:2021/"
