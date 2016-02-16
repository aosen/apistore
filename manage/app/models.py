# -*- coding: utf-8 -*-

import time
import hashlib
import random

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

class UserInfo(models.Model):
    """用户信息表"""
    userauth = models.CharField(verbose_name="用户认证码", unique=True, max_length=30)
    createtime = models.DateField(verbose_name='创建时间')

class Userlog(models.Model):
    """用户log, 只记录用户当天首次登陆"""
    userid = models.IntegerField(verbose_name="用户ID")
    logintime = models.DateField(verbose_name="登陆日期")

class First(models.Model):
    """小说一级分类"""
    firstname = models.CharField(verbose_name="一级分类", max_length=20, unique=True) #一级分类名称
    updatetime = models.DateField(verbose_name='更新时间') #修改时间
    createtime = models.DateField(verbose_name='创建时间') #创建时间

class Second(models.Model):
    """小说二级分类"""
    secondname = models.CharField(verbose_name="二级分类", max_length=20, unique=True) #二级分类名称
    updatetime = models.DateField(verbose_name='更新时间') #修改时间
    createtime = models.DateField(verbose_name='创建时间') #创建时间 

class Novel(models.Model):
    """小说简介数据表"""
    title = models.CharField(verbose_name="标题", max_length=200) #小说
    firstid = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类
    secondid = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类
    author = models.CharField(verbose_name="作者", max_length=50, db_index=True) #作者
    introduction = models.TextField(verbose_name="作品简介") #作品简介
    picture = models.CharField(verbose_name="图片", max_length=200) #图片
    novelsource = models.CharField(verbose_name="原文地址", max_length=200, unique=True) #原文地址
    novelpv = models.IntegerField(verbose_name="小说阅读量", default=0) #小说阅读数
    novelcollect = models.IntegerField(verbose_name="小说收藏量", default=0)  #小说收藏量
    createtime = models.DateField(verbose_name='创建时间') #小说的首次抓去或上传时间

class Collectrank(models.Model):
    """小说收藏量排名"""
    novelid = models.IntegerField(verbose_name="小说ID")
    firstid = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类id
    secondid = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类id
    novelpv = models.IntegerField(verbose_name="小说阅读量")
    novelcollect = models.IntegerField(verbose_name="小说收藏量")  #小说收藏量
    createtime = models.DateField(verbose_name='创建时间')

class Clickrank(models.Model):
    """小说点击排名"""
    novelid = models.IntegerField(verbose_name="小说ID")
    firstid = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类id
    secondid = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类id
    novelpv = models.IntegerField(verbose_name="小说阅读量")
    novelcollect = models.IntegerField(verbose_name="小说收藏量")  #小说收藏量
    createtime = models.DateField(verbose_name='创建时间')

class Recommendlist(models.Model):
    """小说推荐列表 json格式的"""
    """
    {
        "classname": "类型名称", 
        "firstnovel": "第一本小说id",
        "secondtosix": [
            {
                "novelid": "第二本小说id",
                "desc": "第二本小说描述",
            },
            ...
        ],
        "other": [novelid...],
    }
    """
    recommendlist = models.TextField(verbose_name="推荐列表") #推荐列表
    updatetime = models.DateTimeField(verbose_name='更新时间') #修改时间
    createtime = models.DateField(verbose_name='创建时间') #创建时间

class Content(models.Model):
    """小说内容，由爬虫抓取获得"""
    novelid = models.IntegerField(verbose_name="小说ID", db_index=True)
    title = models.CharField(verbose_name="标题", max_length=200, db_index=True) #小说
    firstid = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类id
    secondid = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类id
    chapter = models.IntegerField(verbose_name="序列", db_index=True) #章节
    subtitle = models.CharField(verbose_name="副标题", max_length=200, db_index=True) #副标题
    text = models.TextField(verbose_name="正文") #小说正文
    contentsource = models.CharField(verbose_name="原文地址", max_length=200, db_index=True) #原文地址
    createtime = models.DateField(verbose_name='创建时间')

class Indexlist(models.Model):
    """小说索引信息"""
    key = models.BinaryField(verbose_name="Key")
    value = models.BinaryField(verbose_name="Value")

class Requestlist(models.Model):
    """请求列表"""
    name = models.CharField(verbose_name="爬虫", max_length=20)
    requ = models.TextField(verbose_name="请求")
    createtime = models.DateField(verbose_name="创建时间")

class System(models.Model):
    """系统配置"""
    k = models.CharField(verbose_name="key", max_length=20)
    v = models.CharField(verbose_name="value", max_length=20)
