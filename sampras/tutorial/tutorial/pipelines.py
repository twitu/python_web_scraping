# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            req = scrapy.Request(image_url)
            req.meta['img_path'] = item['image_paths']
            yield req

    def file_path(self, request, response, info=None):
        print response.headers
        return os.path.join(request.meta['img_path'][0])

    def item_completed(self, results, item, info):
        image_paths = item['image_paths']
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item
