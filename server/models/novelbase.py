# -*- coding: utf-8 -*-

from base import Base


class NovelBase(Base):
    """novel model基础类"""
    def __init__(self):
        pass


    def loadAllTag(self):
        sql = "SELECT * FROM tag"
        return self.db.query(sql)


    def loadAllFirstTag(self, second):
        sql = "SELECT * FROM tag WHERE second=%s"
        return self.db.query(sql, second)


    def loadAllSecondTag(self, first):
        sql = "SELECT * FROM tag WHERE first=%s"
        return self.db.query(sql, first)


    def loadFirstSecondTag(self, first, second):
        sql = "SELECT * FROM tag WHERE first=%s AND second=%s"
        return self.db.query(sql, first, second)


    def loadNovelList(self, first, second, page, limit):
        sql = "SELECT * FROM novel WHERE first=%s AND second=%s LIMIT %s,%s"
        return self.db.query(sql, first, second, (page-1)*limit, limit)


    def loadNovelIntroduction(self, novelid):
        sql = "SELECT * FROM novel WHERE id=%s"
        return self.db.query(sql, novelid)


    def loadNovelChapter(self, id):
        sql = "SELECT * FROM content WHERE novelid=%s ORDER BY chapter"
        return self.db.query(sql, id)


    def loadNovelContent(self, chapterid):
        sql = "SELECT * FROM content WHERE id=%s"
        return self.db.query(sql, chapterid)

    def loadPrevNext(self, chapter):
        """根据chapterid获取上一章节的chapterid和下一章节的chapterid"""
        p = n = 0
        sql = "SELECT * FROM chapter WHERE chapter=%s"
        pre = self.db.get(sql, chapter-1)
        nex = self.db.get(sql, chapter+1)
        if not pre:
            p = pre['id']
        if not nex:
            n = nex['id']
        return p, n


    def addNovelPv(self, novelid):
        sql = "UPDATE novel SET novelpv=novelpv+1 WHERE id=%s"
        self.db.execute(sql, novelid)
        return self.loadNovelIntroduction(novelid)

    def loadNovelRank(self, page, limit):
        """获取小说排名列表"""
        sql = "SELECT * FROM novelrank LIMIT %s,%s"
        return self.db.query(sql, (page-1)*limit, limit)

