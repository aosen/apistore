# -*- coding: utf-8 -*-

import tornado.web
from controllers.novelhandler import GetTagList
from controllers.novelhandler import GetNovelList
from controllers.novelhandler import GetNovelChapter
from controllers.novelhandler import GetNovelIntroduction
from controllers.novelhandler import GetNovelContent
from controllers.novelhandler import NovelClick
from controllers.novelhandler import GetNovelRank
from controllers.novelhandler import NovelSearch
from controllers.novelhandler import NovelDownload
from controllers.newshandler import GetSinaGirl
from controllers.newshandler import GetNews
from controllers.cuthandler import Cut
from controllers.searchhandler import SearchAction , IndexAction
from controllers.indexhandler import Index
from controllers.gotyehandler import GotyeToken
from controllers.userauthhandler import RegisterAction , CheckUser

urlpatterns = [
    (r"/", tornado.web.RedirectHandler, {"url":"https://aosen.github.io/apistore/", "permanent":False}),

    (r"/taglist/", GetTagList),
    (r"/novellist/", GetNovelList),
    (r"/novelintroduction/", GetNovelIntroduction),
    (r"/novelchapter/", GetNovelChapter),
    (r"/novelcontent/", GetNovelContent),
    (r"/novelclick/", NovelClick),
    (r"/novelrank/", GetNovelRank),
    (r"/novelsearch/", NovelSearch),
    (r"/noveldownload/", NovelDownload),

    (r"/newsgirlpic/", GetSinaGirl),
    (r"/news/", GetNews),

    (r"/cut/", Cut),
    (r"/index/", IndexAction),
    (r"/search/", SearchAction),

    (r"/imtoken/", GotyeToken),

    (r"/register/",RegisterAction),
    (r"/checkuser/", CheckUser),

    (r"/test/", Index),
        ]
