# -*- coding: utf-8 -*-
#models的基类

import torndb
import Queue

from settings import DATABASES, logger


#class PoolDB(object):
#    """数据库连接池"""
    #判断连接池对象
#    pooldb = None

#    @staticmethod
#    def _initPool(max_connect=10, addr=None, name=None, user=None, password=None, max_idle_time=7 * 3600,
#                  connect_timeout=0, time_zone="+0:00", charset = "utf8", sql_mode="TRADITIONAL"):
#        """初始化数据库连接池,返回池对象"""
#        pooldb = Queue.Queue(maxsize = max_connect)
#        for _ in range(max_connect):
#            conn = torndb.Connection(addr, name, user=user, password=password, max_idle_time=max_idle_time,
#                                     connect_timeout=connect_timeout, time_zone=time_zone,
#                                     charset = charset, sql_mode=sql_mode)
#            pooldb.put(conn)
#        return pooldb

#    @classmethod
#    def open(cls, max_connect=10, addr=None, name=None, user=None, password=None, max_idle_time=7 * 3600,
#                  connect_timeout=0, time_zone="+0:00", charset = "utf8", sql_mode="TRADITIONAL"):
#        if not cls.pooldb:
#            cls.pooldb = cls._initPool(max_connect=max_connect, addr=addr, name=name, user=user, password=password,
#                                       max_idle_time=max_idle_time, connect_timeout=connect_timeout,
#                                       time_zone=time_zone,charset = charset, sql_mode=sql_mode)
#        conn = cls.pooldb.get()
#        logger.info(str(conn._db))
#        if conn._db == None:
#            conn.reconnect()
#        return conn

#    @classmethod
#    def close(cls, conn):
#        if cls.pooldb:
#            cls.pooldb.put(conn)

class BaseModel(object):
    """models的基类"""

    def __init__(self):
        super(BaseModel, self).__init__()
        """
        self.conn = PoolDB.open(max_connect=DATABASES['MAXCONN'],
                    addr=DATABASES['HOST']+':'+DATABASES['PORT'],
                    name=DATABASES['NAME'],
                    user=DATABASES['USER'],
                    password=DATABASES['PASSWORD'])
        """

    def getAppSercet(self, appid):
        sql = "SELECT * FROM application WHERE id=%s"
        v = self.db.get(sql, int(appid))
        if v:
            return v['appsecret']
        else:
            return None

    @property
    def db(self):
        #目前连接池有bug 感觉
        #return self.conn
        return torndb.Connection(DATABASES['HOST']+':'+DATABASES['PORT'],
                                 DATABASES['NAME'],
                                 user=DATABASES['USER'],
                                 password=DATABASES['PASSWORD'],
                                 max_idle_time=7 * 3600,
                                 connect_timeout=0,
                                 time_zone="+0:00",
                                 charset = "utf8",
                                 sql_mode="TRADITIONAL")
    """
    def __del__(self):
        #管理数据库连接
        PoolDB.close(self.db)
    """
