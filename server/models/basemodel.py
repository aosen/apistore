# -*- coding: utf-8 -*-
#models的基类

import torndb

from settings import DATABASES

class BaseModel(object):
    """models的基类"""

    def __init__(self):
        super(BaseModel, self).__init__()

    def getAppSercet(self, appid):
        sql = "SELECT * FROM application WHERE id=%s"
        v = self.db.get(sql, int(appid))
        if v:
            return v['appsecret']
        else:
            return None

    @property
    def db(self):
        #此处后期需要改为连接池,将数据库连接放在启动服务器的时候
        return torndb.Connection(
                DATABASES['HOST']+':'+DATABASES['PORT'], 
                DATABASES['NAME'],
                user=DATABASES['USER'], 
                password=DATABASES['PASSWORD']
                )