# -*- coding: utf-8 -*-
import os.path
import socket
import logging

logger = logging.getLogger('crossapp')

DEBUG = True
#模板目录
TEMPLATE_PATH = "/home/zhen/aosencloud/1/crossapp/template/" 
#静态文件目录
STATIC_PATH = "/home/zhen/aosencloud/1/crossapp/static/" 
#数据库信息
HOME_PATH = os.getcwd()
if socket.gethostname() == 'zhangzhen':
    DATABASES = {
            'NAME': 'aosencloud',
            'USER': 'root',
            'PASSWORD': 'zhangzhen',
            'HOST': '127.0.0.1',
            'PORT': '3307',
            }
elif socket.gethostname() == 'ubuntu':
    DATABASES = {
            'NAME': 'aosencloud',
            'USER': 'root',
            'PASSWORD': 'zhangzhen',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            }
else:
    DATABASES = {
            'NAME': 'aosencloud',
            'USER': 'root',
            'PASSWORD': 'zhangzhen',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            }
MEMCACHE = {
        'ADDR': '127.0.0.1:11211',
        }
