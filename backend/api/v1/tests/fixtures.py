import pytest
from rest_framework import status
from rest_framework.test import APIClient

from cadastral.tests.test_models import create_cadastral_obj, create_log_obj


"""API clients."""


def client_anon() -> APIClient:
    """Возвращает объект анонимного клиента."""
    return APIClient()


"""Статусы запросов."""

# INFO: список статусов, которые может вернуть сервер,
#       если эндпоинт не доступен по указанному адресу.
URL_MISSED_STATUSES: list = [
    status.HTTP_301_MOVED_PERMANENTLY,
    status.HTTP_302_FOUND,
    status.HTTP_303_SEE_OTHER,
    status.HTTP_307_TEMPORARY_REDIRECT,
    status.HTTP_308_PERMANENT_REDIRECT,
    status.HTTP_404_NOT_FOUND,
    status.HTTP_405_METHOD_NOT_ALLOWED,
    status.HTTP_408_REQUEST_TIMEOUT,
    status.HTTP_409_CONFLICT,
    status.HTTP_410_GONE,
]

STATUS_NOT_ALLOWED: status = status.HTTP_405_METHOD_NOT_ALLOWED


"""Фикстуры."""


# Количество объектов моделей, должны создавать все фикстуры.
TEST_FIXTURES_OBJ_AMOUNT: int = 3


@pytest.fixture()
def create_cadastrals() -> None:
    """Фикстура для наполнения БД заданным числом кадастровых номеров."""
    for i in range(1, TEST_FIXTURES_OBJ_AMOUNT + 1):
        create_cadastral_obj(num=i)
    return


@pytest.fixture()
def create_logs() -> None:
    """Фикстура для наполнения БД заданным числом логов."""
    for i in range(1, TEST_FIXTURES_OBJ_AMOUNT + 1):
        create_log_obj(num=i)
    return


""""Эндпоинты API_V1."""


URL_API_V1: str = '/api/v1/'

URL_HISTORY: str = f'{URL_API_V1}history/'

URL_PING: str = f'{URL_API_V1}ping/'

URL_RESULT: str = f'{URL_API_V1}result/'

URL_QUERY: str = f'{URL_API_V1}query/'


"""Эндпоинты drf_spectacular."""


URL_DOCS: str = '/docs/'

URL_SCHEMA: str = f'{URL_DOCS}schema/'

URL_SWAGGER: str = f'{URL_DOCS}swagger/'
