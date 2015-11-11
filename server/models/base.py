# -*- coding: utf-8 -*-
#models的基类

import torndb

from settings import DATABASES

class Base(object):
    """models的基类"""

    def __init__(self):
        super(Base, self).__init__()

    def getAppSercet(self, appid):
        sql = "SELECT * FROM application WHERE id=%s"
        v = self.db.get(sql, int(appid))
        if v:
            return v['appsecret']
        else:
            return None

    @property
    def db(self):
        return torndb.Connection(
                DATABASES['HOST']+':'+DATABASES['PORT'], 
                DATABASES['NAME'],
                user=DATABASES['USER'], 
                password=DATABASES['PASSWORD']
                )