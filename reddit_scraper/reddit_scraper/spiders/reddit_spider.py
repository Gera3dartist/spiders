from datetime import datetime as dt
import scrapy


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    start_urls = [
        "https://reddit.com"
    ]

    def parse(self, response):
        items = []
        for div in response.css('div.sitetable div.thing'):
            try:
                title = div.css('div.entry p.title a::text').extract_first()
                votes_div = div.css('div.score.unvoted')
                votes = votes_div.css('::attr(title)').extract_first()
                votes = votes or votes_div.css('::text').extract_first()

                items.append({'title': title, 'votes': int(votes)})
            except:
                pass
        if items:
            # timestamp = response.meta['wayback_machine_time'].timestamp()
            timestamp = dt.now().isoformat()
            yield {'timestamp': timestamp, 'items': items}
