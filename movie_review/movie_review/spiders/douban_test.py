# -*- coding: utf-8 -*-
import re
import csv


import scrapy
from scrapy.http import Request


class DouBanSpider(scrapy.Spider):
    name = 'douban_test'

    def start_requests(self):
        url = 'https://movie.douban.com/chart'
        yield Request(url=url)

    def parse(self, response):
        movie_urls = response.xpath('//a[@class="nbg"]/@href').extract()
        for movie_url in movie_urls:
            p = re.compile(r'\d+')
            movie_id = p.findall(movie_url)[0]
            for start in range(0, 200, 20):
                url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P'.format(movie_id, start)

                yield Request(url=url, callback=self.parse_default)

    def parse_default(self, response):
        review_list = response.xpath('//span[@class="short"]/text()').extract()
        print(review_list)
        for review in review_list:
            review = review.strip()
            review = review.replace('\t', '')
            review = review.replace('\n', '')
            review = review.replace('\xa0', '')
            review = review.replace('\ufeff', '')
            review = review.replace('\u200b', '')

            review = re.sub("[^\u4e00-\u9fa5]", '', review)

            if review:
                with open('./data/review_test.csv', 'a+') as f:
                    csv_write = csv.writer(f)
                    data_row = [review]
                    csv_write.writerow(data_row)