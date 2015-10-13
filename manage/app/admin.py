# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Content, Novel, Tag, Application, Girlpic, News

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'appsecret']
    search_fields = ['id', 'appsecret']
    ordering = ['id']
admin.site.register(Application, ApplicationAdmin)

class NovelAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'first', 'second', 'author', 'createtime']
    search_fields = ['id', 'title', 'author']
    ordering = ['-id']
admin.site.register(Novel, NovelAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'novelid', 'chapter', 'first', 'second', 'subtitle', 'createtime']
    search_fields = ['novelid', 'title', 'chapter', 'contentsource']
    ordering = ['-id']
admin.site.register(Content, ContentAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'first', 'second', 'createtime']
    search_fields = ['id', 'first', 'second']
    ordering = ['-id']
admin.site.register(Tag, TagAdmin)

class GirlpicAdmin(admin.ModelAdmin):
    list_display = ['title', 'cl', 'createtime']
    search_fields = ['title']
    ordering = ['-id']
admin.site.register(Girlpic, GirlpicAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'tag', 'createtime']
    search_fields = ['title']
    ordering = ['-id']
admin.site.register(News, NewsAdmin)
