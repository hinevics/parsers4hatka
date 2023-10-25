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


def test_get_price(soup):
    try:
        sys.path.append('../realt')
        from realt import get_price
    except ModuleNotFoundError or ImportError:
        assert False

    actual = get_price(soup_ad=soup)
    assert isinstance(actual, str)
    assert len(actual) > 0


def test_get_update_date(soup):
    try:
        sys.path.append('../realt')
        from realt import get_update_date
    except ModuleNotFoundError or ImportError:
        assert False
    exepted = "13.10.2023"
    actual = get_update_date(soup_ad=soup)
    assert isinstance(actual, str)
    assert len(actual) > 0
    assert actual == exepted


def test_get_chars_dict(soup):
    try:
        sys.path.append('../realt')
        from realt import get_chars_dict
    except ModuleNotFoundError or ImportError:
        assert False
    actual = get_chars_dict(soup_ad=soup)

    keys = actual.keys()

    assert len(keys) > 0

    for k in keys:
        assert actual[k] is not None


def test_get_count_romms(soup):
    try:
        sys.path.append('../realt')
        from realt import get_count_romms, get_chars_dict
    except ModuleNotFoundError or ImportError:
        assert False
    ad_data = {'chars': get_chars_dict(soup)}
    actual = get_count_romms(ad_data)
    assert actual is not None


def test_get_number_floor(soup):
    try:
        sys.path.append('../realt')
        from realt import get_number_floor
    except ModuleNotFoundError or ImportError:
        assert False
    actual = get_number_floor(soup)
    assert actual is not None


def test_parsing_ad(soup):
    try:
        sys.path.append('../realt')
        from realt import parsing_ad
    except ModuleNotFoundError or ImportError:
        assert False
    ad_data = parsing_ad(soup_ad=soup)

    keys = ad_data.keys()

    assert len(keys) > 0

    for k in ad_data.keys():
        value = ad_data[k]

        assert value is not None
