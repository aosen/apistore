# -*- coding: utf-8 -*-

import time
import hashlib
import random

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

"""
创建数据库表

BEGIN;
CREATE TABLE `userinfo` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`userauth` varchar(30) NOT NULL UNIQUE,
`createtime` date NOT NULL
)
;
CREATE TABLE `userlog` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`userid` integer NOT NULL,
`logintime` date NOT NULL
)
;
CREATE TABLE `first` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`firstname` varchar(20) NOT NULL,
`updatetime` date NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `second` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`secondname` varchar(20) NOT NULL,
`updatetime` datetime(6) NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `novel` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`title` varchar(200) NOT NULL,
`firstid` integer NOT NULL,
`secondid` integer NOT NULL,
`author` varchar(50) NOT NULL,
`introduction` longtext NOT NULL,
`picture` varchar(300) NOT NULL,
`novelsource` varchar(300) NOT NULL,
`novelpv` integer NOT NULL,
`novelcollect` integer NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `collectrank` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`novelid` integer NOT NULL,
`firstid` integer NOT NULL,
`secondid` integer NOT NULL,
`novelpv` integer NOT NULL,
`novelcollect` integer NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `clickrank` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`novelid` integer NOT NULL,
`firstid` integer NOT NULL,
`secondid` integer NOT NULL,
`novelpv` integer NOT NULL,
`novelcollect` integer NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `recommendlist` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`recommendlist` longtext NOT NULL,
`updatetime` datetime(6) NOT NULL,
`createtime` date NOT NULL
)
;
CREATE TABLE `content` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
`novelid` integer NOT NULL,
`title` varchar(200) NOT NULL,
`firstid` integer NOT NULL,
`secondid` integer NOT NULL,
`chapter` integer NOT NULL,
`subtitle` varchar(200) NOT NULL,
`text` longtext NOT NULL,
`contentsource` varchar(300) NOT NULL,
`createtime` date NOT NULL
)
;
CREATE INDEX `novel_c399d7e8` ON `novel` (`firstid`);
CREATE INDEX `novel_5b0d0f3e` ON `novel` (`secondid`);
CREATE INDEX `novel_e969df21` ON `novel` (`author`);
CREATE INDEX `collectrank_c399d7e8` ON `collectrank` (`firstid`);
CREATE INDEX `collectrank_5b0d0f3e` ON `collectrank` (`secondid`);
CREATE INDEX `clickrank_c399d7e8` ON `clickrank` (`firstid`);
CREATE INDEX `clickrank_5b0d0f3e` ON `clickrank` (`secondid`);
CREATE INDEX `content_9b8d26f7` ON `content` (`novelid`);
CREATE INDEX `content_9246ed76` ON `content` (`title`);
CREATE INDEX `content_c399d7e8` ON `content` (`firstid`);
CREATE INDEX `content_5b0d0f3e` ON `content` (`secondid`);
CREATE INDEX `content_650f3c59` ON `content` (`chapter`);
CREATE INDEX `content_48ed521f` ON `content` (`subtitle`);

COMMIT;
"""

class UserInfo(models.Model):
    """用户信息表"""
    userauth = models.CharField(verbose_name="用户认证码", unique=True, max_length=30)
    createtime = models.DateField(verbose_name='创建时间')

class Userlog(models.Model):
    """用户log, 只记录用户当天首次登陆"""
    userid = models.IntegerField(verbose_name="用户ID")
    logintime = models.DateField(verbose_name="登陆日期")

class First(models.Model):
    """用户一级分类"""
    firstname = models.CharField(verbose_name="一级分类", max_length=20) #一级分类名称
    updatetime = models.DateField(verbose_name='更新时间') #修改时间
    createtime = models.DateField(verbose_name='创建时间') #创建时间

class Second(models.Model):
    """用户二级分类"""
    secondname = models.CharField(verbose_name="二级分类", max_length=20) #二级分类名称
    updatetime = models.DateTimeField(verbose_name='更新时间') #修改时间
    createtime = models.DateField(verbose_name='创建时间') #创建时间 

class Novel(models.Model):
    """小说简介数据表"""
    title = models.CharField(verbose_name="标题", max_length=200) #小说
    firstid = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类
    secondid = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类
    author = models.CharField(verbose_name="作者", max_length=50, db_index=True) #作者
    introduction = models.TextField(verbose_name="作品简介") #作品简介
    picture = models.CharField(verbose_name="图片", max_length=300) #图片
    novelsource = models.CharField(verbose_name="原文地址", max_length=300) #原文地址
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
    contentsource = models.CharField(verbose_name="原文地址", max_length=300) #原文地址
    createtime = models.DateField(verbose_name='创建时间')
