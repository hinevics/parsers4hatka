"This if module for parsing page kufar"

import requests
from typing import Iterator
import time
import logging
import colorlog
from typing import Any

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages_parser.kufar.config import HEADERS
import pages_parser.kufar.css_selectors as selectors
from pages_parser.kufar import css_class as class_


# format logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
color_format = '%(log_color)s' + log_format
formatter_console = colorlog.ColoredFormatter(color_format)
formatter_file = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# all logs
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)


def get_id_ad(api: str, size: int) -> Iterator[int]:
    """Function for yield id ad of flat.

    Args:
        api (str): url api kufar
        size (int): number of returned if ads

    Yields:
        Iterator[int]: _description_
    """

    url = api.format(size=size)
    ads = requests.get(headers=HEADERS, url=url).json()['ads']
    logger.debug(f"len ads = {len(ads)}")
    for a in ads:
        yield a['i']


def parsing(url_kufar: str, api_kufar: str, size: int = 500, ) -> dict[str, Any]:

    options = FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    data = {}

    for i in get_id_ad(api=api_kufar, size=size):

        ad_data = {}

        url_ad = url_kufar.format(i=i)
        ad_data['url_ad'] = url_ad
        logger.info(f"PARSING {i}")
        logger.debug(f"{url_ad}")

        driver.get(url_ad)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            select_price = soup.select(selector=selectors.PRICE)
            if select_price:
                select_price = select_price[0].text
            else:
                select_price = None
                logger.error("select_price is empty")
            ad_data["price"] = select_price
            logger.debug(f"price={select_price}")
        except Exception:
            logger.error("PROBLEM WITH:\tselect_price")
            ad_data["price"] = None

        try:
            select_adress = soup.select(selector=selectors.ADRESS)
            if select_adress:
                select_adress = select_adress[0].text
            else:
                select_adress = None
                logger.error("select_adress is empty")
            ad_data["adress"] = select_adress
            logger.debug(f"adress={select_adress}")
        except Exception:
            logger.error("PROBLEM WITH:\tselect_adress")
            ad_data["adress"] = None

        try:
            update_date = soup.select(selector=selectors.UPDATE_DATE)
            if update_date:
                update_date = update_date[0].text
            else:
                update_date = None
                logger.error("update_date is empty")
            ad_data["update_date"] = update_date
            logger.debug(f"update_date={update_date}")
        except Exception:
            logger.error("PROBLEM WITH:\tupdate_date")
            ad_data["update_date"] = None

        try:
            count_romms = soup.select(selector=selectors.COUNT_ROOMS)
            if count_romms:
                count_romms = count_romms[0].text
            else:
                count_romms = None
                logger.error("count_romms is empty")
            ad_data["count_romms"] = count_romms
            logger.debug(f"count_romms={count_romms}")
        except Exception:
            logger.error("PROBLEM WITH:\tcount_romms")
            ad_data["count_romms"] = None

        try:
            number_floor = soup.select(selector=selectors.NUMBER_FLOOR)
            if number_floor:
                number_floor = number_floor[0].text
            else:
                logger.error("number_floor is empty")
                number_floor = None
            ad_data["number_floor"] = number_floor
            logger.debug(f"number_floor={number_floor}")
        except Exception:
            logger.error("PROBLEM WITH:\number_floor")
            ad_data["number_floor"] = None

        try:
            chars_dict = {}
            characteristics = soup.select(selector=selectors.CHARS)
            if characteristics:
                finded_characts = characteristics[0].find_all(
                    name='div',
                    attrs={'class': class_.CHARS_CLASS}
                )
                if finded_characts:
                    for div_char in finded_characts:
                        name_char = div_char.find(
                            name='div',
                            attrs={'class': class_.CHARS_NAME_CLASS}
                        )
                        value_char = div_char.find(
                            name='div',
                            attrs={'class': class_.CHARS_VALUE_CLASS}
                        )
                        if name_char and value_char:
                            chars_dict[name_char.text] = value_char.text
                            logger.debug(f"{name_char.text} ---- {value_char.text}")
                        else:
                            logger.error(("name_char or value_char is empty\n"
                                          f"name_char={name_char}, value_char={value_char}"))
                else:
                    logger.error("finded_characts is empry")
            else:
                logger.error("characteristics is empry")
        except Exception:
            logger.error("PROBLEM WITH:\tchars_dict")
            chars_dict = {}
        ad_data['chars'] = chars_dict

        try:
            description = soup.select(selector=selectors.DESC)
            if description:
                description = description[0].text
            else:
                logger.error("description is empty")
                description = None
            ad_data['description'] = description
            logger.debug(f"description={description}")
        except Exception:
            logger.error("PROBLEM WITH:\tdescription")
            ad_data['description'] = None
        try:
            images = soup.select(selector=selectors.IMG)
            if images:
                srcs = [s['src'] for s in images[0].find_all('img')]
                for im in srcs:
                    logger.debug(f"src: {im}")
            else:
                logger.error("images is empty")
                srcs = None
            ad_data['imgs'] = srcs
        except Exception:
            logger.error("PROBLEM WITh:\timages")
            ad_data['imgs'] = None

        data[i] = ad_data
        print('-'*100)
        print(data)
        break
    return data
