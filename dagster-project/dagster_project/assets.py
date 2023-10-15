from dagster import asset

from pages_parser import kufar


@asset
def parser_realt():
    kufar.function_return()


@asset
def parser_kufar():
    pass


@asset
def parser_hata():
    pass


@asset
def parser_domovito():
    pass
