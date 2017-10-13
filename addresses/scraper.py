"""
A tutorial from: https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

"""
import scrapy
import re, os

class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	start_urls = [
		"http://www.in.gov/isdh/reports/LHDs/LHDs_by_county.html",
	]
	root = "http://www.in.gov/isdh/reports/LHDs"

	def parse(self, response):
		SET_SELECTOR = '//map/area'
		for addr in response.xpath(SET_SELECTOR):
			onclick = 'area ::attr(onclick)'
			part = self.get_url(addr.css(onclick).extract_first())
			if not part:
				continue
			yield scrapy.Request(os.path.join(self.root, part), callback=self.parse_address)

# r = list(map(lambda x: re.search(r'\w+/\w+.html', str(x.css('area ::attr(onclick)').extract_first())).group(), res))
# r = list(map(lambda x: re.search(r"\w+/\w+.html", str(x.css('area ::attr(onclick)').extract_first())), res))
# list(map(lambda x: x.css('area ::attr(onclick)').extract_first(), res))

	def parse_address(self, response):
		# extraction part goes here

		try:
			website = response.xpath('body/div/table/tr[2]/td/p[3]/a[2]/text()').extract().pop().strip()
		except:
			website = ''



		tmpl = {
			'First Name': '',
			'Last Name': '',
			'Title': '',
			'Department': '',
			'Addreess 1': '',
			'Address 2': '',
			'City': '',
			'State': '',
			'Zip': '',
			'County': '',
			'Email1': '',
			'Phone': '',
			'Website': website,
			'URL': response.url
		}
		self.get_addr(response, tmpl)
		self.get_email(response, tmpl)
		self.get_phone(response, tmpl)
		self.get_employee(response, tmpl)

		yield tmpl

	def get_url(self, target: str):
		res = re.search(r'\w+/\w+.\w+', str(target))
		if res:
			return res.group()

	def get_addr(self, response, container):
		addr = response.xpath('body/div/table/tr[2]/td/p[1]/text()').extract()
		addr = ', '.join(map(str.strip, addr))
		addr = re.search(r"(^[\d]+[\w\s]+)\,\s([\w\s\w]+),\s([\w]+)\s([\d-]+)", addr)
		if addr:
			tmpl = {
				'Addreess 1': addr.group(1),
				'State': addr.group(3),
				'Zip': addr.group(4)
			}

			tmpl.update({'City': addr.group(2)}) if 'county' not in str.lower(addr.group(2)) \
			else tmpl.update({'Country': addr.group(2)})
			container.update(tmpl)

	def get_email(self, response, container):
		email = response.xpath('body/div/table/tr[2]/td/p[3]/a[1]/text()').extract()
		for idx, el in enumerate(email):
			container.update({'Email{}'.format(idx): el})

	def get_phone(self, response, container):
		try:
			r = response.xpath('body/div/table/tr[2]/td/p[3]/text()').extract().pop(0).strip()
		except:
			r = ''
		container['Phone'] = '-'.join(re.findall(r"\d+", r))

	def get_employee(self, response, container):
		try:
			emp = response.xpath('body/div/table/tr[2]/td/p[2]/text()').extract()\
			or response.xpath('body/div/table/tbody/tr[2]/td/p[2]/text()').extract()
			emp = " ".join(map(str.strip, emp))
			if 'officer' not in emp.lower():
				emp = response.xpath('body/div/table/tr[2]/td/p[1]/text()').extract()
				emp = next(filter(lambda word: 'officer' in word.lower().strip(), emp), '').strip()
		except:
			emp = ''
		emp = ' '.join(map(str.strip, emp.split())).replace('Officer ', '')
		title = re.search(r"(MD|M\.D\.|DO|Dr.)", emp)
		fl_name = re.search(r"([\w\s\.]+),?", emp).group(1)
		f_name, l_name = ' '.join(fl_name.split()[:-1]), fl_name.split()[-1]
		container.update({'employee': emp})
		try:
			container.update({
				'First Name': f_name,
				'Last Name': l_name,
				'Title': title.group(1)
			})
		except:
			pass


	def get_department(self, response, container):
		try:
			department = response.xpath('body/div/table/tr[1]/th/text()').extract().pop(0).strip()
			container['Department'] = department
		except:
			pass


