
'''     Lesson 5
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172 '''

from selenium import webdriver
from pprint import pprint
import time
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
#time.sleep(5)

# --------------------------------------------------------------

#                   Чтение письм

letters = []

link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
)
link = link.get_attribute('href')
driver.get(link)


button_down = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "svg.ico.ico_16-arrow-down.ico_size_s"))
)
try:
    while button_down:

        letter_data = {}
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
        pprint(letters)
        button_down.click()
        time.sleep(2)
except:
    client = MongoClient('localhost', 27017)

    db = client['letters_fom_mailru']

    mails = db.letters

    mails.drop()
    mails.insert_many(letters)