# -*- coding: utf-8 -*-
import re
import csv


import scrapy
from scrapy.http import Request


class DouBanSpider(scrapy.Spider):
    name = 'douban'

    def start_requests(self):
        with open('./data/top.txt', 'r') as f:
            top_list = f.readlines()
        for movie_id in top_list:
            for start in range(0, 200, 20):
                meta = {
                    'sentiment': 1
                }
                movie_id = movie_id.replace('\n', '')
                url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=h'.format(movie_id, start)
                yield Request(url=url, meta=meta)
                meta = {
                    'sentiment': 0
                }
                movie_id = movie_id.replace('\n', '')
                url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=l'.format(
                    movie_id, start)
                yield Request(url=url, meta=meta)

    def parse(self, response):
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
                with open('./data/review.csv', 'a+') as f:
                    csv_write = csv.writer(f)
                    data_row = [response.meta['sentiment'], review]
                    csv_write.writerow(data_row)
