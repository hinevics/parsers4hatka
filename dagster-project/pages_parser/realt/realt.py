from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import URL_REALT


def parsing(url_realt: str, size: int):

    options = FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    for i in range(1, size + 1):
        url = url_realt.format(i=i)
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        div_elements_with_data_index = soup.find_all('div', {'data-index': True})
        print(len(div_elements_with_data_index))
        break


if __name__ == "__main__":
    parsing(
        url_realt=URL_REALT,
        size=2
    )
