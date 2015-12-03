# -*- coding: utf-8 -*-

import time

from basemodel import BaseModel

#docids的范围 1-999999999999
DOCIDSIZE = 1000000000000

class SearchModel(BaseModel):
    def __init__(self):
        super(SearchModel, self).__init__()

    def loadDocids(self, appid, docids):
        """
        根据appid, docids获取开发者所要查找的文档范围
        :param appid: 开发者唯一标识
        :param docids: 查询范围,如果为None 则为全部
        :return: 将所有docids用-连接的字符串
        """
        pass

    def addIndex(self, appid, docid):
        """
        将docid增加到表Doc中
        :param appid:
        :param docid:
        :return: 无返回值
        """
        def doc():
            sql = "SELECT maxdocid FROM doc WHERE appid_id=%s"
            return self.db.get(sql, appid)

        sql1 = "INSERT INTO doc (appid_id, maxdocid, createtime, updatetime) VALUES (%s, %s, %s, %s)"
        sql2 = "UPDATE doc SET maxdocid=%s, updatetime=%s WHERE appid_id=%s"
        now = str(int(time.time()))
        d = doc()
        if not d:
            self.db.insert(sql1, appid, docid, now, now)
        else:
            #如果新的docid比maxdocid大,就update
            maxdocid = d["maxdocid"]
            if int(docid) > maxdocid:
                self.db.update(sql2, docid, now, appid)