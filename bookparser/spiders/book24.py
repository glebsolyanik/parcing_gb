import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/nekhudozhestvennaya-literatura-1345/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(text(), 'Далее')]/@href").extract_first()
        books_links = response.xpath("//a[contains(@class, 'book__image-link js-item-element ddl_product_link')]/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name_b = response.css('h1.item-detail__title::text').extract_first()
        link_b = response.url
        authors_b = response.xpath("//*[contains(text(), 'Автор')]/../span/a/text()").extract_first()
        price_new_b = int(response.xpath("//div[@class='item-actions__prices js-product-card-sticky']/div[@class='item-actions__price']/b/text()").extract_first())
        price_old_b = response.css('div.item-actions__price-old').extract_first()
        rate_b = response.css('span.rating__rate-value::text').extract_first()
        currency_b = 'руб'
        domain_b = 'book24.ru'
        yield BookparserItem(name=name_b, link=link_b, authors=authors_b, price_old=price_new_b,
                             price_new=price_old_b, rate=rate_b, currency=currency_b, domain=domain_b)