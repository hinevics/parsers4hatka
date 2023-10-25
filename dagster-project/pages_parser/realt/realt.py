import re

import logging
import colorlog

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import URL_REALT, URL_REALT_BASE
import css_selectors as selectors

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


def get_title(soup_ad: BeautifulSoup) -> str | None:
    """Функция для получения заголовка объявления

    Args:
        soup_ad (BeautifulSoup): bs4 объект html страницы

    Returns:
        str | None: заголовок объявления
    """
    try:
        title = soup_ad.select(
            selector=selectors.TITLE
        )
        if title:
            title = title[0].text
        else:
            logger.warning("Value title is empty. Using None as the value.")
            title = None
    except Exception as e:
        logger.error(
            (f"Exception:\t{e}"
                "Problem with processing title."
                "Using None as the value.")
        )
        title = None
    return title


def get_description(soup_ad: BeautifulSoup) -> str | None:
    """Функция возращает описание объявления.

    Args:
        soup_ad (BeautifulSoup): bs4 объект html страницы

    Returns:
        str | None: Описание объявления.
    """
    try:
        description = soup_ad.select(
            selector=selectors.DESC)
        if description:
            description = ' '.join([i.text for i in description])
        else:
            logger.warning("Value description is empty. Using None as the value.")
            description = ''
    except Exception as e:
        logger.error(
            (f"Exception:\t{e}"
                "Problem with processing description."
                "Using None as the value.")
        )
        description = ''
    return description


def get_description_note(soup_ad) -> str:
    try:
        description_note = soup_ad.select(
            selector=selectors.DESC_NOTE)
        if description_note:
            description_note = ' '.join([i.text for i in description_note])
        else:
            logger.warning("Value description_note is empty")
            description_note = ''
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing description_note."
                "Using '' as the value.")
        )
        description_note = ''
    return description_note


def get_adress(soup_ad) -> str | None:  # TODO: Переписать так чтоб город  и адресс были раздельно
    # Тоже самое добавить и в другие парсера
    try:
        adress = soup_ad.select(
            selector=selectors.ADRESS
        )
        if adress:
            adress: str = adress[0].text
            adress = re.sub(string=adress, repl=" ", pattern=r"\xa0")
        else:
            logger.warning("Value adress is empty")
            adress = None
        logger.debug(f"adress:\t{adress}")
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing adress."
                "Using None as the value.")
        )
        adress = None
    return adress


def get_price(soup_ad) -> str | None:
    try:
        price = soup_ad.select(
            selector=selectors.PRICE
        )
        if price:
            price = price[0].text
        else:
            logger.warning("Value price is empty.")
            price = None
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing price."
                "Using None as the value.")
        )
        price = None
    return price


def get_update_date(soup_ad) -> str | None:
    try:
        update_date = soup_ad.select(
            selector=selectors.UPDATE_DATE
        )
        if update_date:
            update_date = update_date[0].text
        else:
            update_date = None
            logger.warning("update_date is empty.")
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing update_date."
                "Using None as the value.")
        )
        update_date = None
    return update_date


def get_chars_dict(soup_ad) -> dict:
    chars_dict = {}
    try:
        characteristics = soup_ad.select(
            selector=selectors.CHAR
        )
        if characteristics:
            li_params = characteristics[0].find_all('li')
            if li_params:
                for li in li_params:
                    name_params = li.find_all('span')
                    value_params = li.find_all('p')
                    if name_params and value_params:
                        name_params = name_params[0].text.lower()
                        value_params = value_params[0].text
                        logger.debug(
                            (f'Add params name={name_params}'
                                'and params value={value_params}'))
                        chars_dict[name_params] = value_params
                    else:
                        logger.warning((f"Params is empty.\nname_params:\t{name_params},"
                                        f"value_params:\t{value_params}"))
            else:
                logger.warning("Value li_params is empty.")
        else:
            logger.warning("Value characteristics is empty.")
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing characteristics."
                "Using {} as the value.")
        )
    return chars_dict


def get_count_romms(ad_data: dict) -> str | None:
    try:
        if count_romms := ad_data.get('chars', {}).get("количество комнат", None):
            logger.debug(f"count_romms:\t{count_romms}")
            ad_data["count_romms"] = count_romms
        else:
            logger.warning("Value count_romms is empty.")
            count_romms = None
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing count_romms."
                "Using None as the value.")
        )
        count_romms = None
    return count_romms


def get_number_floor(soup_ad) -> str | None:
    try:
        number_floor = soup_ad.select(
            selector=selectors.NUMBER_FLOOR
            )
        if number_floor:
            number_floor = number_floor[0].text
        else:
            logger.warning("number_floor is empry")
    except Exception as e:
        logger.error(
            (f"Exception:{e}"
                "Problem with processing number_floor."
                "Using None as the value.")
        )
        number_floor = None
    return number_floor


def parsing_ad(soup_ad: Tag) -> dict | bool:
    ad_data = {}

    # title

    title = get_title(soup_ad=soup_ad)
    ad_data['title'] = title
    logger.debug(f'title={title}')

    # description
    description = get_description(soup_ad=soup_ad)
    logger.debug(f"description={description}")
    ad_data['description'] = ''

    # description_note
    description_note = get_description_note(soup_ad=soup_ad)
    logger.debug(f"description_note={description_note}")
    ad_data["description"] = ad_data["description"] + ' ' + description_note

    # adress
    adress = get_adress(soup_ad=soup_ad)
    logger.debug(f"adress={adress}")
    ad_data['adress'] = adress

    # price
    price = get_price(soup_ad=soup_ad)
    logger.debug(f"price={price}")
    ad_data["price"] = price

    # update_date
    update_date = get_update_date(soup_ad=soup_ad)
    logger.debug(f"update_date={update_date}")
    ad_data["update_date"] = update_date

    chars_dict = get_chars_dict(soup_ad=soup_ad)
    logger.debug(f"chars_dict={chars_dict}")
    ad_data['chars'] = chars_dict

    # count_romms
    count_romms = get_count_romms(ad_data=ad_data)
    logger.debug(f"count_romms={count_romms}")
    ad_data["count_romms"] = count_romms

    # number_floor
    number_floor = get_number_floor(soup_ad=soup_ad)
    ad_data['number_floor'] = number_floor
    logger.debug(f'number_floor={number_floor}')

    return ad_data


def parsing(url_realt: str, size: int):

    options = FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    data = {}

    # create list urls for ads
    for i in range(1, size + 1):
        logger.info(f"Start parsing page {i}")
        try:
            url = url_realt.format(i=i)
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            div_elements_with_data_index = soup.find_all('div', {'data-index': True})
            for ad in div_elements_with_data_index:

                href = ad.find_all('a')[0]

                try:
                    number_ad = re.search(
                        pattern=r'\№(?P<number>\d+)',
                        string=href['aria-label']).group('number')
                except Exception as e:
                    logger.error(
                        (f"Exception:\t{e}"
                            "Problem with parsing number ad."
                            "Complete of ad processing. Go to the next ad.")
                    )

                if str(number_ad) in data.keys():
                    logger.warning(
                        (f"Ad number {number_ad} exists."
                            f"Completion of ad processing. Go to the next ad.")
                    )
                    continue

                url_ad = URL_REALT_BASE + href['href']

                logger.debug(f"url_ad:\t{url_ad}")

                try:
                    driver.get(url_ad)
                    soup_ad = BeautifulSoup(driver.page_source, 'html.parser')
                except Exception as e:
                    logger.error(
                        (f"Exception:\t{e}"
                            f"Problem with load page {url_ad}"
                            "Complete of ad processing. Go to the next ad.")
                    )
                    continue
                logger.info(f"Start parsing ad {ad}")
                ad_data = parsing_ad(soup_ad=soup_ad)
                ad_data["url_ad"] = url_ad
                data[number_ad] = ad_data
            break
        except Exception as e:
            logger.error(
                f"Exception:\t{e}"
            )
            logger.error(f"Critical error. Completion of page {i} processing. Go to the next page")


if __name__ == "__main__":
    parsing(
        url_realt=URL_REALT,
        size=2
    )
