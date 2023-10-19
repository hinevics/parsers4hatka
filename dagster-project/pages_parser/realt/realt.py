import re

import logging
import colorlog

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import URL_REALT, URL_REALT_BASE


# format logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
color_format = '%(log_color)s' + log_format
formatter_console = colorlog.ColoredFormatter(color_format)
formatter_file = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# all logs
logger = logging.getLogger('logger-realt')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)


def parsing(url_realt: str, size: int):

    options = FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    data = {}

    # create list urls for ads
    for i in range(1, size + 1):
        try:
            url = url_realt.format(i=i)
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            div_elements_with_data_index = soup.find_all('div', {'data-index': True})
            for ad in div_elements_with_data_index:
                href = ad.find_all('a')[0]
                number_ad = re.search(
                    pattern=r'\№(?P<number>\d+)',
                    string=href['aria-label']).group('number')

                if str(number_ad) in data.keys():
                    logger.warning(f"Ad number {number_ad} exists.")
                    continue

                ad_data = {}

                url_ad = URL_REALT_BASE + href['href']
                ad_data["url_ad"] = url_ad

                logging.debug(f"url_ad:\t{url_ad}")

                driver.get(url_ad)
                soup_ad = BeautifulSoup(driver.page_source, 'html.parser')

                # title
                try:
                    title = soup_ad.select('h1.order-1')  # TODO: fix selector
                    if title:
                        title = title[0].text
                    else:
                        logger.warning("title is empty")
                        title = None

                except Exception:
                    logger.error("PROBLEM WITH:\ttitle")
                    title = None
                ad_data['title'] = title
                logging.debug(f'title:\t{title}')

                # description
                try:
                    description = soup_ad.select(
                        'section.bg-white:nth-child(3) > div:nth-child(2)')  # TODO: fix selector
                    if description:
                        description = ' '.join([i.text for i in description])
                    else:
                        logger.warning("description is empty")
                        description = ''
                except Exception:
                    logger.error("PROBLEM WITH:\tdescription")
                    description = ''
                logging.debug(f"description:\t{description}")
                ad_data['description'] = ''

                # description_note
                try:
                    description_note = soup_ad.select(
                        'section.bg-white:nth-child(6) > div:nth-child(2)')
                    if description_note:
                        description_note = ' '.join([i.text for i in description_note])
                    else:
                        logger.warning("description_note is empty")
                        description_note = ''
                except Exception:
                    logger.error("PROBLEM WITH:\tdescription_note")
                    description_note = ''
                logging.debug(f"description_note:\t{description_note}")
                ad_data["description"] = ad_data["description"] + ' ' + description_note

                # adress
                try:
                    adress = soup_ad.select(
                        selector=r'li.md\:w-auto'
                    )
                    if adress:
                        adress = adress[0].text
                    else:
                        logger.warning("adress is empty")
                        adress = None
                    logger.debug(f"adress:\t{adress}")
                except Exception:
                    logger.error("PROBLEM WITH:\tadress")
                    adress = None
                logger.debug(f"adress:\t{adress}")
                ad_data['adress'] = adress

                # price
                try:
                    price = soup_ad.select(
                        r'.md\:items-center > div:nth-child(1) > h2:nth-child(1)')
                    if price:
                        price = price[0].text
                    else:
                        logger.warning("price is empty.")
                        price = None
                except Exception:
                    logger.error("PROBLEM WITH:\tprice")
                    price = None
                logging.debug(f"price:\t{price}")
                ad_data["price"] = price

                # update_date
                try:
                    update_date = soup_ad.select(  # TODO: Вынесети selector в отдельный модуль
                        selector=r'div.text-caption:nth-child(2) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
                    )
                    if update_date:
                        update_date = update_date[0].text
                    else:
                        update_date = None
                        logger.warning("update_date is empty.")
                except Exception:
                    logger.error("PROBLEM WITH:\tupdate_date")
                    update_date = None
                logger.debug(f"update_date:\t{update_date}")
                ad_data["update_date"] = update_date

                chars_dict = {}
                try:
                    characteristics = soup_ad.select(r'ul.w-full:nth-child(2)')
                    if characteristics:
                        li_params = characteristics[0].find_all('li')
                        if li_params:
                            for li in li_params:
                                name_params = li.find_all('span')
                                value_params = li.find_all('p')
                                if name_params and value_params:
                                    chars_dict[name_params.lower()] = value_params
                                else:
                                    logger.warning((f"Params is empty.\nname_params:\t{name_params},"
                                                    f"value_params:\t{value_params}"))
                        else:
                            logger.warning("li_params is empty.")
                    else:
                        logger.warning("characteristics is empty.")
                except Exception:
                    logging.error("PROBLEM WITH:\tcharacteristics")
                logger.debug(f"chars_dict:\t{chars_dict}")
                ad_data['chars'] = chars_dict

                count_romms = ad_data['chars']["количество комнат"]
                logging.debug(f"count_romms:\t{count_romms}")
                ad_data["count_romms"] = count_romms

                # number_floor
                try:
                    number_floor = soup_ad.select(
                        selector=r'div.last\:mr-0:nth-child(3) > div:nth-child(1)'
                        )
                    if number_floor:
                        number_floor = number_floor[0].text
                    else:
                        logging.warning("number_floor is empry")
                except Exception:
                    logging.error("PROBLEM WITH:\tcount_romms")
                    ad_data = None
                ad_data['number_floor'] = number_floor
                logging.debug(f' -- number_floor:\t{number_floor}')
                break
            break
        except Exception as e:
            logger.error(
                f"PROBLEM WITH PAGE:\t{i}. Exception:\t{e}"
            )


if __name__ == "__main__":
    parsing(
        url_realt=URL_REALT,
        size=2
    )
