from dagster import asset

from pages_parser.kufar import kufar
from dagster_project.config import URL_KUFAR, API_URL_KUFAR


@asset
def parser_realt():
    pass


@asset
def parser_kufar():
    kufar.parsing(
        url_kufar=URL_KUFAR,
        api_kufar=API_URL_KUFAR,
        size=10
    )


@asset
def parser_hata():
    pass


@asset
def parser_domovito():
    pass
