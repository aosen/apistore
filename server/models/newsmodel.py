# -*- coding: utf-8 -*-

from basemodel import BaseModel

class NewsModel(BaseModel):
    """News models基类"""
    def __init__(self):
        super(NewsModel, self).__init__()

    def loadSinaGirlPic(self, cl, page, limit):
        if cl:
            #sql = """SELECT * FROM girlpic WHERE cl=%s ORDER BY -createtime LIMIT %s, %s"""
            #return self.db.query(sql, cl, (page-1)*limit, limit)
            sql = """SELECT * FROM girlpic ORDER BY -createtime LIMIT 1000"""
            dictlist = self.db.query(sql)
            l = []
            for dict in dictlist:
                if dict['cl'] == cl:
                    l.append(dict)
            return l[(page-1)*limit: (page-1)*limit + limit]
        else:
            sql = """SELECT * FROM girlpic ORDER BY -createtime LIMIT %s, %s"""
            return self.db.query(sql, (page-1)*limit, limit)

    def loadNews(self, tag, page, limit):
        sql = "SELECT * FROM news ORDER BY id DESC limit 1000"
        dictlist = self.db.query(sql)
        l = []
        for dict in dictlist:
            if dict['tag'] == tag:
                l.append(dict)
        return l[(page-1)*limit : (page-1)*limit + limit]
        #sql = "SELECT * FROM news WHERE tag=%s ORDER BY -createtime LIMIT %s, %s"
        #return self.db.query(sql, tag, (page-1)*limit, limit)
