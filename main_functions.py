import requests
from pprint import pprint
from lxml import html
from main_variables import header, link_yandex, link_lenta
from pymongo import MongoClient
# Функции для парсера news

def request_to_yandex_news():

    response = requests.get(f'{link_yandex}', headers=header)
    dom = html.fromstring(response.text)

    full_news_yandex = []

    # main_news


    items = dom.xpath("//div[contains(@class, 'story__topic')]")

    for item in items:
        news = {}

        # name
        name = item.xpath(".//h2[@class='story__title']//a[contains(@class, 'link')]/text()")
        news['name'] = name

        # header
        head = item.xpath(".//a[contains(@class, 'rubric-label')]/text()")
        news['head'] = head

        # link to news
        link = str(item.xpath(".//h2[@class='story__title']//a[contains(@class, 'link')]/@href"))
        link = link.replace(u"['", u'')
        link = link.replace(u"']", u'')
        news['link'] = 'https://yandex.ru' + link

        # link of website
        main_link = link_yandex
        news['main_link'] = main_link

        full_news_yandex.append(news)

    return full_news_yandex




def request_to_lenta_news():
    full_news_lenta = []

    response = requests.get(f'{link_lenta}', headers=header)
    dom = html.fromstring(response.text)

    items = dom.xpath("//section[contains(@class, 'js-top-seven')]//div[contains(@class, 'item')]")

    for item in items:
        news = {}


        # name
        name = str(item.xpath("./h2/a/text()|./a/text()"))
        name = name.replace(u'\\xa0', u' ')
        name = name.replace(u"['", u'')
        name = name.replace(u"']", u'')
        news['name'] = name

        # date and time
        time = item.xpath("./h2/a/time/@datetime|./a/time/@datetime")
        news['time'] = time
        full_news_lenta.append(news)

        # link
        link = item.xpath("./h2/a/@href|./a/@href")
        if 'https://' not in link:
            news['link'] = 'https://lenta.ru' + str(link).replace(u"['", '').replace(u"']", '')
        else:
            news['link'] = link

        # main_link
        news['main_link'] = link_lenta

    return full_news_lenta

full_db_news = []

full_news_lenta = request_to_lenta_news()
full_news_yandex = request_to_yandex_news()


full_db_news.append(full_news_lenta)
full_db_news.append(full_news_yandex)


client = MongoClient('localhost', 27017)

db = client['database_news']

def load_news_to_db(full_db_news):

    news = db.news

    #news.insert_many(full_db_news[0])
    #news.insert_many(full_db_news[1])

    for new in news.find({}):
        pprint(new)

    return full_db_news

load_news_to_db(full_db_news)
