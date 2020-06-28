# -*- coding: utf-8 -*-
import scrapy
from home_work2.items import HomeWork2Item
from scrapy.selector import Selector

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        yield scrapy.Request(url = self.start_urls[0], callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for movie in movies:
            item = HomeWork2Item()
            item['movie_name'] = movie.xpath('./div[1]/span[1]/text()').extract_first()
            item['movie_type'] = movie.xpath('./div[2]/text()[2]').extract_first().strip()
            item['movie_time'] = movie.xpath('./div[4]/text()[2]').extract_first().strip()
            yield item