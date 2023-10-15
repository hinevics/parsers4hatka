"This if module for parsing page kufar"

from bs4 import BeautifulSoup
from selenium import webdriver

from config import EXECUTABLE_PATH, URL_KUFAR


def parsing():
    driver = webdriver.Firefox()
    print(driver)
    # driver.get(URL_KUFAR)


if __name__ == "__main__":
    parsing()
