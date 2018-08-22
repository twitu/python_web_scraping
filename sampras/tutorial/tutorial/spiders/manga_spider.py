import scrapy
# from tutorial.items import imgitem
class imgitem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


class QuotesSpider(scrapy.Spider):
    name = "manga"

    def start_requests(self):
        base_url = "http://mangafreak.com"
        manga = "monster"
        chapter = "42"

        yield scrapy.Request(url=base_url + "/" + manga + "/chapter-" + chapter + "/full", callback=self.parse)

    def parse(self, response):
        for i,url in enumerate(response.css('div.chapter-container img::attr(src)').extract(),1):

            item = imgitem()
            item['image_urls'] = [url]
            item['image_paths'] = ["/" + str(i) + ".jpg"]

            yield item




