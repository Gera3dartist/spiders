from scrapy.spider import Spider
from tutsplus.items import TutsplusItem
from scrapy.http import Request



class TutsPlusSpider(Spider):
	name = 'tutsplus'
	start_urls = ['http://code.tutsplus.com/']

	def parse(self, response):

		titles = response.xpath('//a[contains(@class, "posts__post-title")]/h1/text()').extract()
		for title in titles:
			yield {"title": title}

		next_page = response.xpath('//a[@class="pagination__button pagination__next-button"]/@href').extract_first()
		tuts = response.xpath('//a[@href="/tutorials"]/@href').extract_first()
		if tuts:
			yield response.follow(tuts, self.parse)
		if next_page:
			yield response.follow(next_page, self.parse)
