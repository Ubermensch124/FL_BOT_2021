from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests


def check_new():
    # URL = 'https://www.fl.ru/projects/'
    #
    # options = Options()
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\Mark\Desktop\full_bot_second\venv\chromedriver.exe')
    #
    # driver.get(URL)
    #
    # open_list = driver.find_element_by_class_name('b-combo__arrow')
    # open_list.click()
    # open_list = driver.find_elements_by_class_name('b-combo__item-inner ')
    # list_of_work = []
    # open_list = open_list[200:300]
    # for i in open_list:
    #     if len(i.text) > 2:
    #         list_of_work.append(i.text)
    # return list_of_work
    d = {'Разработка сайтов': 2, 'Программирование': 5, 'Тексты': 8, 'Дизайн и Арт': 3, 'Аудио/Видео': 11, 'Реклама и маркетинг': 12,
         'Аутсорсинг и консалтинг': 13, 'Разработка игр': 16, 'Анимация и флеш': 19, 'Переводы': 7, 'Фотография': 10, '3D Графика': 9,
         'Инжиниринг': 20, 'Оптимизация (SEO)': 6, 'Архитектура/Интерьер': 14, 'Обучение и консультации': 22, 'Полиграфия': 17,
         'Менеджмент': 1, 'Мобильные приложения': 23, 'Сети и инфросистемы': 24}
    return d


def get_screen(url):
    URL = url

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options,
                              executable_path=r'C:\Users\Mark\Desktop\full_bot_second\venv\chromedriver.exe')

    driver.get(URL)
    driver.save_screenshot(r'screen_news.png')
