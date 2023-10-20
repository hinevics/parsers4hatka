# TODO: Разработка тестов для тестовой страницы!
# Добавить возможность подменять странницу по которой будет выполняться запрос
import sys

from bs4 import BeautifulSoup

from test_config import TEST_URL, TEST_URL2


def test_load_page(driver):
    # test how work fixture driver
    driver.get(TEST_URL)
    soup_ad = BeautifulSoup(driver.page_source, 'html.parser')
    assert soup_ad is not None


def test_soup(soup):
    # test how work fixture soup
    assert soup is not None


def test_import_get_title():
    # test function get_title
    try:
        sys.path.append('../realt')
        from realt import get_title
        get_title
        assert True
    except ModuleNotFoundError:
        assert False


def test_get_title_normal(soup):
    sys.path.append('../realt')
    from realt import get_title

    actual = get_title(soup)
    expected = "Стильная трехкомнатная квартира в тихом центре г.Минска"
    assert actual is not None
    assert len(actual) > 0
    assert actual == expected


def test_get_description_normal(soup):
    sys.path.append('../realt')
    from realt import get_description

    actual = get_description(soup_ad=soup)

    assert actual is not None
    assert isinstance(actual, str)
    assert len(actual) > 0


def test_get_description_note_without_note(soup):
    sys.path.append('../realt')
    from realt import get_description_note

    actual = get_description_note(soup_ad=soup)
    assert isinstance(actual, str)
    assert actual == ''


def test_get_description_note_with_note(driver):
    try:
        sys.path.append('../realt')
        from realt import get_description_note
    except ModuleNotFoundError or ImportError:
        assert False

    driver.get(TEST_URL2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    actual = get_description_note(soup_ad=soup)

    assert isinstance(actual, str)
    assert len(actual) > 0


def test_get_adress(soup):
    try:
        sys.path.append('../realt')
        from realt import get_adress
    except ModuleNotFoundError or ImportError:
        assert False
    actual = get_adress(soup_ad=soup)

    assert isinstance(actual, str)
    assert len(actual) > 0
    assert str(actual) == 'г. Минскпросп. Независимости, 85/г'
