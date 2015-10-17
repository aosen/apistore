# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http.request import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

import robot
import robot.utils

class ImagePipeline(ImagesPipeline):
    """下载图片"""
    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get(self.IMAGES_URLS_FIELD, [])]

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
            return item

    def file_path(self, request, response=None, info=None):
        f_path = super(ImagePipeline, self).file_path(request, response, info)
        f_path = f_path.replace('full', self.spiderinfo.spider.name, 1)#从meta取出title作为文件夹名称
        return f_path

@robot.utils.cache_error
class RobotPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        "爬虫名称需要跟相应爬虫文件同名"
        return getattr(getattr(robot, item.module), spider.name).Process().process(item)
