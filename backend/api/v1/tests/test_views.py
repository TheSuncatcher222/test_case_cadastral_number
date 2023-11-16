import json

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from api.v1.tests.fixtures import (  # noqa (F401)
    client_anon,
    create_cadastrals, create_logs,
    URL_HISTORY, URL_PING, URL_QUERY, URL_RESULT,
)
from cadastral.models import CadastralNumber, LogsHistory


@pytest.mark.django_db
class TestCheckPing():
    """Производит тест корректности настройки эндпоинта check_ping."""

    def test_check_ping(self) -> None:
        """Тест POST-запроса на проверку доступности сервера."""
        response = client_anon().post(path=URL_PING)
        assert response.status_code == status.HTTP_200_OK
        data: dict = json.loads(response.content)
        assert data == {'message': 'API функционирует.'}
        return

    @pytest.mark.parametrize('method', ['delete', 'get', 'patch', 'put'])
    def test_check_ping_not_allowed(self, method: str) -> None:
        """
        Тест запрета на CRUD запросы к эндпоинту check_ping:
            - DELETE
            - GET
            - PATCH
            - PUT
        """
        client: APIClient = client_anon()
        response = getattr(client, method)(path=URL_PING)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        return


@pytest.mark.django_db
class TestGetHistory():
    """Производит тест корректности настройки эндпоинта get_history."""

    def test_get_history(self, create_logs) -> None:  # noqa (F811)
        """Тест GET-запроса на получение истории запросов."""
        cadastral_number: str = LogsHistory.objects.all().first().cadastral
        response = client_anon().generic(
            method="GET",
            path=URL_HISTORY,
            data=json.dumps({"number": cadastral_number}),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        data: dict = json.loads(response.content)
        assert data == [
            {'cadastral': '12:12:123456:03',
             # INFO: Freezegun не работает при POSTзапросах.
             'datetime': data[0].get('datetime'),
             'method': 'method_3',
             'path': '/path_3/',
             'request_data': 'request_data_3',
             'response_data': 'response_data_3',
             'status_code': 3
             },
        ]
        return

    @pytest.mark.parametrize('method', ['delete', 'patch', 'post', 'put'])
    def test_get_history_not_allowed(self, method: str) -> None:
        """
        Тест запрета на CRUD запросы к эндпоинту get_history:
            - DELETE
            - PATCH
            - POST
            - PUT
        """
        client: APIClient = client_anon()
        response = getattr(client, method)(URL_HISTORY)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        return


@pytest.mark.django_db
class TestGetQuery():
    """Производит тест корректности настройки эндпоинта get_query."""

    def test_get_query(self) -> None:
        """Тест POST-запроса на добавление кадастрового номера в БД."""
        cadastral_count_init: int = CadastralNumber.objects.all().count()
        response = client_anon().post(
            path=URL_QUERY,
            data=json.dumps(
                {"number": "12:12:123456:12",
                 "latitude": "12.1",
                 "longitude": "12.123456",
                 },
            ),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        cadastral_count_new: int = CadastralNumber.objects.all().count()
        assert cadastral_count_new == cadastral_count_init + 1
        data: dict = json.loads(response.content)
        assert data == {
            'number': '12:12:123456:12',
            'latitude': 12.1,
            'longitude': 12.123456,
            'status': None
        }
        cadastral_ids: list[int] = CadastralNumber.objects.all(
        ).values_list(
            'id', flat=True
        )
        latest_cadastral: CadastralNumber = CadastralNumber.objects.get(
            id=max(cadastral_ids),
        )
        assert latest_cadastral.number == data.get('number')
        assert latest_cadastral.latitude == data.get('latitude')
        assert latest_cadastral.longitude == data.get('longitude')
        assert latest_cadastral.status == data.get('status')
        return

    def test_get_query_invalid(self) -> None:
        """
        Тест POST-запроса на добавление кадастрового номера в БД
        с невалидными данными запроса."""
        cadastral_count_init: int = CadastralNumber.objects.all().count()
        response = client_anon().post(
            path=URL_QUERY,
            data=json.dumps(
                {"number": "1",
                 "latitude": "1.12345678",
                 "longitude": "1.12345678",
                 },
            ),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        cadastral_count_new: int = CadastralNumber.objects.all().count()
        assert cadastral_count_new == cadastral_count_init
        data: dict = json.loads(response.content)
        assert data == {
            'number': [
                'Укажите корректный кадастровый номер вида XX:XX:XXXXXX:XX.'
            ],
            'latitude': [
                'Укажите корректные координаты широты вида XX.XXXXXX.'
            ],
            'longitude': [
                'Укажите корректные координаты долготы вида XX.XXXXXX.'
            ]
        }
        return

    @pytest.mark.parametrize('method', ['delete', 'get', 'patch', 'put'])
    def test_get_query_not_allowed(self, method: str) -> None:
        """
        Тест запрета на CRUD запросы к эндпоинту get_query:
            - DELETE
            - GET
            - PATCH
            - PUT
        """
        client: APIClient = client_anon()
        response = getattr(client, method)(path=URL_PING)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        return


@pytest.mark.django_db
class TestGetResult():
    """Производит тест корректности настройки эндпоинта get_result."""

    def test_get_result(self, create_cadastrals) -> None:  # noqa (F811)
        """Тест GET-запроса на проверку статуса кадастрового номера."""
        cadastral: CadastralNumber = CadastralNumber.objects.all().first()
        response = client_anon().generic(
            method="GET",
            path=URL_RESULT,
            data=json.dumps({"number": cadastral.number}),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        data: dict = json.loads(response.content)
        assert data == {
            'number': cadastral.number,
            'latitude': cadastral.latitude,
            'longitude': cadastral.longitude,
            'status': cadastral.status
        }
        return

    @pytest.mark.parametrize(
        ('data', 'status_code', 'expected_data'),
        [
            (
                {
                    "number": "1",
                },
                status.HTTP_400_BAD_REQUEST,
                {
                    'number': [
                        'Укажите корректный кадастровый номер вида XX:XX:XXXXXX:XX.'  # noqa (E501)
                    ],
                },
            ),
            (
                {
                    "number": "99:99:999999:99",
                },
                status.HTTP_404_NOT_FOUND,
                {
                    'detail': 'Страница не найдена.',
                },
            ),
        ],
    )
    def test_get_result_invalid(
            self, create_cadastrals, data, status_code, expected_data  # noqa (F811)
        ) -> None:  # noqa (E125)
        """
        Тест GET-запроса на проверку статуса кадастрового номера
        с невалидными данными запроса.
        """
        response = client_anon().generic(
            method="GET",
            path=URL_RESULT,
            data=json.dumps(data),
            content_type='application/json',
        )
        assert response.status_code == status_code
        data: dict = json.loads(response.content)
        assert data == expected_data
        return

    @pytest.mark.parametrize('method', ['delete', 'get', 'patch', 'put'])
    def test_get_result_not_allowed(self, method: str) -> None:
        """
        Тест запрета на CRUD запросы к эндпоинту get_result:
            - DELETE
            - GET
            - PATCH
            - PUT
        """
        client: APIClient = client_anon()
        response = getattr(client, method)(path=URL_PING)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        return
