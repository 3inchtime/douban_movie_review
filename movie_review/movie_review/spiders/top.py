# -*- coding: utf-8 -*-
import re


import scrapy
from scrapy.http import Request


class DouBanSpider(scrapy.Spider):
    name = 'top'

    def start_requests(self):
        for i in range(0, 250, 25):
            url = 'https://movie.douban.com/top250?start={}&filter='.format(str(i))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        movie_urls = response.xpath('//div[@class="pic"]/a/@href').extract()
        for movie_url in movie_urls:
            p = re.compile(r'\d+')
            movie_id = p.findall(movie_url)[0]

            with open('./data/top.txt', 'a+') as f:
                f.write(movie_id)
                f.write('\n')

            print(movie_id)
