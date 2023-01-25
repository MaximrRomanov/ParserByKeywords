import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
import logging


def fake_ua() -> UserAgent:
    ua = UserAgent()
    return ua.random

# params: queryList - list of
def get_keyword(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)
    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))
    return keywords

# initialization webdriver
def init_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(f'user-agent={fake_ua()}')

    seleniumwire_options = {
        'addr': 'django',
        'proxy': {
            'http': 'socks5://np436186:n38e7m82@elena.ltespace.com:14384',
            'https': 'socks5://np436186:n38e7m82@elena.ltespace.com:14384',
            'no_proxy': 'localhost,django,127.0.0.1'
        }
    }

    browser = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=chrome_options,
        seleniumwire_options=seleniumwire_options
    )

    browser.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return browser


def parser(queryList: list, domens_list: list):
    browser = init_driver()
    keywords = get_keyword(queryList)
    try:
        for keyword in keywords:
            url = "https://yandex.ru/search/?text=" + keyword
            browser.get(url)
            a_tags = browser.find_elements(By.XPATH, "")
            # list of hrefs
            href_list = []
            for a_tag in a_tags:
               href = a_tag.get_attribute("href")
               href_list.append(href)
            print(href_list)

    except Exception as ex:
        logging.exception(ex)

    if browser:
        browser.quit()


def main():
    queryList = [
        'Кухни в Питере',
        'купить Дом в Краснодаре',
        'кухни Зов в Майкопе',
        'собака красивая сторойная',
        'как научиться программировать'
    ]
    keywords = get_keyword(queryList)
    print(keywords)


main()
