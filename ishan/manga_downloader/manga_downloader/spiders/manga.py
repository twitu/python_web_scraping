# -*- coding: utf-8 -*-
import scrapy

class MangaSpider(scrapy.Spider):
    name = 'manga'
    allowed_domains = ['http://mangafreak.com']
    base_url = "http://mangafreak.com/"
    chapter_url = "http://mangafreak.com/{}/chapter-{}/full"

    def __init__(self, manga=None, start=0, end=0, *args, **kwargs):
        super(MangaSpider, self).__init__(*args, **kwargs)

        print "check arguments"
        if manga and start and end:
            self.manga_name = manga
            self.start_chapter = int(start)
            self.end_chapter = int(end)
        else:
            raise ValueError("Please mention manga name as per website, starting and ending chapters.")

    def start_requests(self):
        # generate url for manga from starting to ending chapter in full mode
        return [scrapy.Request(url=MangaSpider.chapter_url.format(self.manga_name, chapter_number), 
            callback=self.page_parser) for chapter_number in range(self.start_chapter, self.end_chapter+1)]

    def page_parser(self, response):
        image_url = response.css("div.chapter-container img::attr(src)").extract()
        # yield [scrapy.Request(url=image_url, callback=self.image_parser) for url in image_url]
        yield {"image_urls": image_url}     
