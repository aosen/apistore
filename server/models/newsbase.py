# -*- coding: utf-8 -*-

from base import Base

class NewsBase(Base):
    """News models基类"""
    def __init__(self):
        pass

    def loadSinaGirlPic(self, cl, page, limit):
        if cl:
            sql = """SELECT * FROM girlpic WHERE cl=%s LIMIT %s, %s"""
            return self.db.query(sql, cl, (page-1)*limit, limit)
        else:
            sql = """SELECT * FROM girlpic LIMIT %s, %s"""
            return self.db.query(sql, (page-1)*limit, limit)

    def loadNews(self, tag, page, limit):
        sql = "SELECT * FROM news WHERE tag=%s LIMIT %s, %s"
        return self.db.query(sql, tag, -(page-1)*limit, -limit)
