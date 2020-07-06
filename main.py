from main_functions import request_to_yandex_news, request_to_lenta_news, full_db_news
from pprint import pprint
from pymongo import MongoClient
from main_functions import *
'''                    Lesson 4

1) Написать приложение, которое собирает основные новости с сайтов 
news.mail.ru, lenta.ru, yandex.news Для парсинга использовать xpath.
 Структура данных должна содержать: название источника, 
 наименование новости, ссылку на новость, дата публикации

2) Сложить все новости в БД. '''

load_news_to_db(full_db_news)











