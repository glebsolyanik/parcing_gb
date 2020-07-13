import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = \
        ['https://www.labirint.ru/genres/2993/']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_links = response.xpath("//div[@id = 'catalog']//div[@class='product-cover']//div[@class='product-cover__cover-wrapper']/a[@class='cover']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response: HtmlResponse):
        name_b = response.css('h1::text').extract_first()
        link_b = response.url
        authors_b = response.xpath("//div[@class='authors']/a/text()").extract_first()
        price_old_b = int(response.xpath("//div[@class='buying-priceold-val']/span/text()").extract_first())
        price_new_b = response.xpath("//div[@class='buying-pricenew-val']/span[@class='buying-pricenew-val-number']/text()").extract_first()
        rate_b = float(response.css('div#rate::text').extract_first())
        currency_b = 'руб'
        domain_b = 'labirint.ru'
        yield BookparserItem(name=name_b, link=link_b, authors=authors_b, price_old=price_old_b,
                             price_new=price_new_b, rate=rate_b, currency=currency_b, domain=domain_b)


