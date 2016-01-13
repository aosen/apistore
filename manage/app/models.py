# -*- coding: utf-8 -*-

import time
import hashlib
import random

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 


class Application(models.Model):
    """使用web api的app信息"""

    _secret = hashlib.md5(str(time.time()) + str(random.randint(1, int(time.time())))).hexdigest()

    appsecret = models.CharField(max_length=32, unique=True, default=_secret)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'开发者'
        verbose_name_plural = u'开发者'
        db_table = 'application'

    def __unicode__(self):
        return self.appsecret

class Doc(models.Model):
    """appid与docid列表"""
    appid = models.OneToOneField(Application, verbose_name="AppID", unique=True)
    maxdocid = models.BigIntegerField(verbose_name="文档列表")
    createtime = models.CharField(verbose_name='创建时间', default=str(int(time.time())), max_length=10)
    updatetime = models.CharField(verbose_name='更新时间', default=str(int(time.time())), max_length=10)

    class Meta:
        verbose_name = u'文档列表'
        verbose_name_plural = u'文档列表'
        db_table = 'doc'

class Novel(models.Model):
    """小说简介数据表"""
    title = models.CharField(verbose_name="标题", max_length=200, unique=True) #小说
    first = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类
    second = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类
    author = models.CharField(verbose_name="作者", max_length=50, db_index=True) #作者
    introduction = models.TextField(verbose_name="作品简介") #作品简介
    picture = models.CharField(verbose_name="图片", max_length=300) #图片
    novelsource = models.CharField(verbose_name="原文地址", max_length=300) #原文地址
    novelpv = models.IntegerField(verbose_name="小说阅读量", default=0)
    novelcollect = models.IntegerField(verbose_name="小说收藏量", default=0)  #小说收藏量
    createtime = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'小说标题'
        verbose_name_plural = u'小说标题'
        db_table = 'novel'

    def __unicode__(self):
        return self.title

class Clickrank(models.Model):
    """小说点击排名"""

class Novelrank(models.Model):
    """小说排名数据表"""
    novelid = models.IntegerField(verbose_name="小说ID")
    title = models.CharField(verbose_name="标题", max_length=200) #小说
    first = models.IntegerField(verbose_name="一级分类") #一级分类
    second = models.IntegerField(verbose_name="二级分类") #二级分类
    picture = models.CharField(verbose_name="图片", max_length=300) #图片
    author = models.CharField(verbose_name="作者", max_length=50) #作者
    novelpv = models.IntegerField(verbose_name="小说阅读量")
    createtime = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'小说排名'
        verbose_name_plural = u'小说排名'
        db_table = 'novelrank'

    def __unicode__(self):
        return self.title

class Content(models.Model):
    """小说内容，由爬虫抓取获得"""
    novelid = models.IntegerField(verbose_name="小说ID", db_index=True)
    title = models.CharField(verbose_name="标题", max_length=200, db_index=True) #小说
    first = models.IntegerField(verbose_name="一级分类", db_index=True) #一级分类
    second = models.IntegerField(verbose_name="二级分类", db_index=True) #二级分类
    chapter = models.IntegerField(verbose_name="序列", db_index=True) #章节
    subtitle = models.CharField(verbose_name="副标题", max_length=200, db_index=True) #副标题
    text = models.TextField(verbose_name="正文") #小说正文
    contentsource = models.CharField(verbose_name="原文地址", max_length=300) #原文地址
    createtime = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'小说内容'
        verbose_name_plural = u'小说内容'
        db_table = 'content'

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    """分类列表"""
    CHOICES = [
                [0, '女'],
                [1, '男']
            ]
    first = models.IntegerField(verbose_name="一级分类", choices=CHOICES ,db_index=True) #0 女生 1 男生
    second = models.CharField(verbose_name="二级分类", max_length=200, unique=True) # 二级分类为详细的分类信息
    createtime = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'小说分类'
        verbose_name_plural = u'小说分类'
        db_table = 'tag'

    def __unicode__(self):
        return self.title

class UserInfo(models.Model):
    """开发者的用户信息表"""
    appid = models.ForeignKey(Application, verbose_name="AppID")
    username = models.CharField(verbose_name="用户名", max_length=20)
    createtime = models.CharField(verbose_name='创建时间', default=str(int(time.time())), max_length=10)
    updatetime = models.CharField(verbose_name='更新时间', default=str(int(time.time())), max_length=10)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'
        db_table = 'userinfo'

    def __unicode__(self):
        return self.username
