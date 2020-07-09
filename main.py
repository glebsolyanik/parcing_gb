
'''     Lesson 5
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172 '''

from selenium import webdriver
from pprint import pprint
import time
from pymongo import MongoClient

from main_variables import *

#               Вход в mail

# создаю драйвер mail.ru
driver = webdriver.Chrome('./chromedriver')
driver.get(main_link)

# ввожу логин почты
login = driver.find_element_by_id('mailbox:login')
login.send_keys('study.ai_172')

# нажимаю кнопку 'ввести пароль'
password_button = driver.find_element_by_id('mailbox:submit')
password_button.click()

# ввожу пароль
write_password = driver.find_element_by_id('mailbox:password')
write_password.send_keys('NextPassword172')

# кнопка ввод
input_button = driver.find_element_by_id('mailbox:submit')
input_button.click()

# --------------------------------------------------------------

#                   Чтение письм

letters = []

time.sleep(10)
letter = driver.find_elements_by_xpath("//div[@class='dataset__items']/a")
links = []
for lett in letter:
    link_to_letter = lett.get_attribute('href')
    links.append(link_to_letter)

for link in links[16:17]:

    letter_data = {}

    # переходим по ссылке письма
    driver.get(link)

    time.sleep(10)

    # запись названия темы письма
    letter_name = driver.find_element_by_xpath("//h2")
    letter_name = letter_name.text
    letter_data['name'] = letter_name

    # полный текст письма
    letter_text = driver.find_element_by_xpath("//div[@class='letter__body']")
    letter_data['text'] = str(letter_text.text).replace(u"\n", u'')

    # время
    time_data = driver.find_element_by_xpath("//div[@class='letter__date']")
    letter_data['time'] = time_data.text

    # запись данных в список
    letters.append(letter_data)
    #pprint(letters)

    time.sleep(5)

client = MongoClient('localhost', 27017)

db = client['letters_fom_mailru']

mails = db.letters

mails.drop()
mails.insert_many(letters)

for mail in mails:
    pprint(mail)











