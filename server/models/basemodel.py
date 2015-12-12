# -*- coding: utf-8 -*-
#models的基类

import torndb
import Queue

from settings import DATABASES, logger

class ManageDB(object):
    """数据库连接池"""
    conn = None

    @classmethod
    def open(cls, max_connect=10, addr=None, name=None, user=None, password=None, max_idle_time=7 * 3600,
                  connect_timeout=0, time_zone="+0:00", charset = "utf8", sql_mode="TRADITIONAL"):
        if cls.conn is None:
            cls.conn = torndb.Connection(addr, name, user=user, password=password, max_idle_time=max_idle_time,
                                     connect_timeout=connect_timeout, time_zone=time_zone,
                                     charset = charset, sql_mode=sql_mode)
        return cls.conn

class BaseModel(object):
    """models的基类"""

    def __init__(self):
        super(BaseModel, self).__init__()
        self.conn = ManageDB.open(max_connect=DATABASES['MAXCONN'],
                    addr=DATABASES['HOST']+':'+DATABASES['PORT'],
                    name=DATABASES['NAME'],
                    user=DATABASES['USER'],
                    password=DATABASES['PASSWORD'])

    def getAppSercet(self, appid):
        sql = "SELECT * FROM application WHERE id=%s"
        v = self.db.get(sql, int(appid))
        if v:
            return v['appsecret']
        else:
            return None

    @property
    def db(self):
        return self.conn
