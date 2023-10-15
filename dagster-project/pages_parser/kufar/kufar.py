"This if module for parsing page kufar"

import requests
from typing import Iterator
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# from pages_parser.kufar.config import API_URL_KUFAR, HEADERS, URL_KUFAR
# import pages_parser.kufar.css_selectors as selectors

from config import API_URL_KUFAR, HEADERS, URL_KUFAR
import css_selectors as selectors


def get_id_ad(api: str, size: int) -> Iterator[int]:
    """Function for yield id ad of flat.

    Args:
        api (str): url api kufar
        size (int): number of returned if ads

    Yields:
        Iterator[int]: _description_
    """

    url = api.format(size=size)
    data = requests.get(headers=HEADERS, url=url).json()['ads']
    print("len ads = ", len(data))
    for ad in data:
        yield ad['i']


def parsing(url_kufar: str, api_kufar: str, size: int = 500, ):

    options = FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    for i in get_id_ad(api=api_kufar, size=size):

        url_ad = url_kufar.format(i=i)
        print(url_ad)

        driver.get(url_ad)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        select_price = soup.select(selector=selectors.PRICE)
        print(select_price[0].text)

        select_adress = soup.select(selector='.styles_text__0UyQ7')
        print(select_adress[0].text)

        update_date = soup.select(selector=r'.styles_date_gallery__tAtHD')
        print(update_date[0].text)

        count_romms = soup.select(selector=r'div.styles_element__6_lmi:nth-child(1)')
        print(count_romms[0].text)

        number_floor = soup.select(selector=r'div.styles_element__6_lmi:nth-child(2)')
        print(number_floor[0].text)

        characteristics = soup.select(selector=r'.styles_parameter_block__47ovj')
        finded_characts = characteristics[0].find_all('div', {'class': 'styles_parameter_wrapper__MHS22'})
        for div_char in finded_characts:
            name_char = div_char.find('div', {'class': 'styles_parameter_label__3nY0_'})
            value_char = div_char.find('div', {'class': 'styles_parameter_value__8v4Ow'})

            print(name_char.text, '----', value_char.text)
        break


if __name__ == "__main__":
    parsing(
        url_kufar=URL_KUFAR,
        api_kufar=API_URL_KUFAR,
        size=10
    )
