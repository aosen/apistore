# -*- coding: utf-8 -*-

from basemodel import BaseModel
import utils


class NovelModel(BaseModel):
    """novel model基础类"""
    def __init__(self):
        super(NovelModel, self).__init__()


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

    def loadPrevNext(self, chapter, novelid):
        """根据chapterid获取上一章节的chapterid和下一章节的chapterid"""
        p = n = 0
        sql = "SELECT * FROM content WHERE chapter=%s AND novelid=%s"
        chapter_next = chapter_pre = chapter
        nex = pre = None
        #如果i超过3次，则说明已经到达末位
        i = 3
        while i != 0:
            chapter_next += 1
            nex = self.db.get(sql, chapter_next, novelid)
            if nex:
                break
        while chapter_pre != 0:
            chapter_pre -= 1
            pre = self.db.get(sql, chapter_pre, novelid)
            if pre:
                break

        if pre:
            p = pre['id']
        if nex:
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

    def getNovelDocMaxId(self, appid):
        """获取小说最大id"""
        sql = "SELECT maxdocid FROM doc WHERE appid_id=%s"
        docmaxid = self.db.get(sql,appid)["maxdocid"]
        return utils.decodeDocid(appid, docmaxid)

    def getNovelListById(self, novelidlist):
        """根据小说id列表加载小说详情列表"""
        """
        SQL: select * from table where id IN (3,6,9,1,2,5,8,7);
        这样的情况取出来后，其实，id还是按1,2,3,4,5,6,7,8,9,排序的，但如果我们真要按IN里面的顺序排序怎么办？
        SQL能不能完成？是否需要取回来后再foreach一下？其实mysql就有这个方法
        sql: select * from table where id IN (3,6,9,1,2,5,8,7) order by field(id,3,6,9,1,2,5,8,7);
        出来的顺序就是指定的顺序了。
        """
        l = ", ".join([str(id) for id in novelidlist])
        sql = """
        SELECT id, title, first, second, author, introduction, picture, novelpv FROM novel WHERE
        id IN (%s) ORDER BY FIELD (id, %s);
        """ % (l, l)
        return self.db.query(sql)