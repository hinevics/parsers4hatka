from dagster import asset

from pages_parser.kufar import kufar
from dagster_project.config import URL_KUFAR, API_URL_KUFAR, PATH_DATA_KUFAR
from saver.saver_data_parsed import saver


@asset
def parser_realt():
    pass


@asset
def parser_kufar():
    data = kufar.parsing(
        url_kufar=URL_KUFAR,
        api_kufar=API_URL_KUFAR,
        size=2
    )
    return data


@asset
def data_save(parser_kufar):
    saver(parser_kufar, path=PATH_DATA_KUFAR)


@asset
def parser_hata():
    pass


@asset
def parser_domovito():
    pass
