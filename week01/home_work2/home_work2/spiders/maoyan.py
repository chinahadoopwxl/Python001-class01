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
        movies = Selector(response=response).xpath('//dl[@class="movie-list"]//dd[position()<=10]')
        for movie in movies:
            item = HomeWork2Item()

            minfos = movie.xpath('.//div[@class="movie-hover-info"]//div[contains(@class,"movie-hover-title")]')
            item['movie_name'] = minfos[1].xpath('./span[@class="name "]/text()').extract_first()
            item['movie_type'] = minfos[2].xpath('text()').extract()[1].strip('\n').strip()
            item['movie_time'] = minfos[4].xpath('text()').extract()[1].strip('\n').strip()
            print("电影名称：{} 电影类型：{} 上映时间：{}".format(item['movie_name'], item['movie_type'], item['movie_time']))
            yield item