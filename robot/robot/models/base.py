# -*- coding: utf-8 -*-

#robot的基础模型, 基于torndb

import torndb
from robot.settings import DATABASES

class Base(object):
    """所有models的基类"""
    def __init__(self):
        pass

    @property
    def db(self):
        try:
            db = torndb.Connection(
                DATABASES['HOST']+':'+DATABASES['PORT'], 
                DATABASES['NAME'],
                user=DATABASES['USER'], 
                password=DATABASES['PASSWORD']
                )
        except Exception as e:
            print str(e)
            raise ValueError(1)
        else:
            return db

