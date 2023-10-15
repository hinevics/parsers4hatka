"This if module for parsing page kufar"

from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from config import URL_KUFAR, API_URL_KUFAR, HEADERS
import css_selectors as selectors


def parsing(size: int = 500):

    url = API_URL_KUFAR.format(size=size)
    data = requests.get(headers=HEADERS, url=url).json()
    print(len(data))
    print('-'*100)
    print(len(data['ads']))
    i = data['ads'][0]['i']
    print('-'*100)
    print(i)
    url_ad = URL_KUFAR.format(i=i)
    driver = webdriver.Firefox()
    print(driver)
    driver.get(url_ad)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    select_price = soup.select(selector=selectors.PRICE)
    print(select_price[0].text)


if __name__ == "__main__":
    parsing()
