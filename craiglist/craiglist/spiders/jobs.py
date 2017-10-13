# -*- coding: utf-8 -*-
import scrapy
from  scrapy import Request

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craiglist.org']
    start_urls = ['http://newyork.craiglist.org/search/egr']

    def parse1(self, response):
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        for title in titles:
            yield {'title': title}

    def parse2(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            yield {'title': title}

    def parse3(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            yield {'title': title, 'address': address}
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            yield{'URL':absolute_url, 'Title':title, 'Address':address}

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)

