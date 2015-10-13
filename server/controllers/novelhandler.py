# -*- coding: utf-8 -*-

import json
import datetime


from tornado.web import RequestHandler

from models.novelbase import NovelBase
import utils
from utils import json_success, json_failed, cache_error
import const

class Novel(RequestHandler):
    novel = NovelBase()


class GetTagList(Novel):
    """获取小说分类"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        first = self.get_argument("first", None)
        second = self.get_argument("second", None)
        if first == None and second == None:
            tag_list = self.novel.loadAllTag()
        elif first != None and second == None:
            tag_list = self.novel.loadAllSecondTag(first)
        elif first == None and second != None:
            tag_list = self.novel.loadAllFirstTag(second)
        else:
            tag_list = self.novel.loadFirstSecondTag(first, second)
        result = [{'first': v['first'], 'second': v['id'], 'name': v['second']} for v in tag_list]
        self.write(json_success(result)) 


class GetNovelList(Novel):
    """获取某分类下的小说列表"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        first = self.get_argument("first", None)
        second = self.get_argument("second", None)
        page = self.get_argument("page", None)
        page = 1 if not page else int(page)
        limit = self.get_argument("limit", None)
        limit = const.NOVEL_LIMIT if not limit else int(limit)
        if not first or not second:
            raise ValueError(1)
        else:
            novel_list = self.novel.loadNovelList(first, second, page, limit)
            result = [{'novelid': v['id'], 'title': v['title'], 'novelpv': v['novelpv'], 'author': v['author'], 'introduction': v['introduction'], 'picture': "/static/spider/" + v['picture']} for v in novel_list]
            self.write(json_success(result)) 


class GetNovelIntroduction(Novel):
    """获取小说简介"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        novelid = self.get_argument("novelid", None)
        if not novelid:
            raise ValueError(1)
        else:
            intro = self.novel.loadNovelIntroduction(int(novelid))
            print intro.__len__()
            if intro.__len__() != 1:
                raise ValueError(500)
            else:
                result = {'title': intro[0]['title'], 'novelid': intro[0]['id'], 'author': intro[0]['author'], 'picture': "/static/spider/"+intro[0]['picture'], 'introduction': intro[0]['introduction']}
            self.write(json_success(result))


class GetNovelChapter(Novel):
    """获取小说的章节列表"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        novelid = self.get_argument("novelid", None)
        if not novelid:
            raise ValueError(1)
        else:
            chapter_list = self.novel.loadNovelChapter(int(novelid))
            result = [{'subtitle': v['subtitle'], 'chapter': i, 'chapterid': v['id']} for i, v in enumerate(chapter_list, 1)]
            self.write(json_success(result))


class GetNovelContent(Novel):
    """获取小说的内容"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        chapterid = self.get_argument("chapterid", None)
        if not chapterid:
            raise ValueError(1)
        else:
            c = self.novel.loadNovelContent(int(chapterid))
            if c.__len__() != 1:
                raise ValueError(500)
            else:
                result = {'title': c[0]['title'], 'subtitle': c[0]['subtitle'], 'novelid': c[0]['novelid'], 'content': c[0]['text']}
                self.write(json_success(result))

class NovelClick(Novel):
    """计算小说点击数"""

    def get(self):
        return self.post()

    @cache_error
    @utils.checkSign
    def post(self):
        novelid = self.get_argument("novelid", None)
        novelid = int(novelid) if novelid else None
        if not novelid:
            raise ValueError(1)
        else:
            if self.novel.loadNovelIntroduction(novelid).__len__() != 1:
                raise ValueError(6)
            n = self.novel.addNovelPv(novelid)[0]
            result = {'novelid': n['id'], 'novelpv': n['novelpv']}
            self.write(json_success(result))
