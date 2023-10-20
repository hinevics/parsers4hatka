import pytest

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from test_config import TEST_URL


@pytest.fixture
def driver():
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver


@pytest.fixture
def soup(driver):
    driver.get(TEST_URL)
    soup_ad = BeautifulSoup(driver.page_source, 'html.parser')
    return soup_ad
