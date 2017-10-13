"""
A tutorial from: https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

"""
import scrapy

class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = [
		"http://brickset.com/sets/year-2016",
		'https://brickset.com/sets/year-2017'
	]

	def parse(self, response):
		SET_SELECTOR = '.set'
		for legoset in response.css(SET_SELECTOR):
			NAME_SELECTOR = 'h1 a ::text'
			PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
			MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
			IMAGE_SELECTOR = 'img ::attr(src)'
			yield {
				'name': ' '.join(map(str.strip, legoset.css(NAME_SELECTOR).getall())),
				'pieces': legoset.xpath(PIECES_SELECTOR).extract_first(),
				'minifigs': legoset.xpath(MINIFIGS_SELECTOR).extract_first(),
				'image': legoset.css(IMAGE_SELECTOR).extract_first(),
			}

		NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
		if next_page:
			yield scrapy.Request(response.urljoin(next_page),
				callback=self.parse)
