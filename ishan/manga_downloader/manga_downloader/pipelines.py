# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.contrib.pipeline.images import ImagesPipeline


class MangaDownloaderPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
    	url_parts = request.url.split("/")
    	image_name = url_parts[-1]
    	chapter_name = url_parts[-2]
    	manga_name = url_parts[-3]

        return os.path.join(manga_name, chapter_name, image_name)
