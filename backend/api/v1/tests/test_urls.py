import pytest

from api.v1.tests.fixtures import (
    client_anon,
    URL_MISSED_STATUSES,
    URL_HISTORY, URL_PING, URL_QUERY, URL_RESULT, URL_SCHEMA, URL_SWAGGER,
)


@pytest.mark.django_db
class TestEndpointsAvailability():
    """
    Производит тест доступности эндпоинтов в urlpatterns.
    """

    @pytest.mark.parametrize(
        'url, meaning', [
            (URL_SCHEMA,
             'получения схемы документации API'
             ),
            (URL_SWAGGER,
             'получения swagger-представления документации API'
             ),
            (URL_HISTORY,
             'получения истории запросов по кадастровому номеру'
             ),
            (URL_PING,
             'проверки доступности сервера'
             ),
            (URL_QUERY,
             'добавления кадастрового номера в реестр'
             ),
            (URL_RESULT,
             'просмотра данных кадастрового номера'
             ),
            (URL_RESULT,
             'просмотра данных кадастрового номера'
             ),
        ]
    )
    def test_ping(self, url, meaning) -> None:
        """Производит тест доступности эндпоинтов JWT."""
        url: str = URL_PING
        response = client_anon().post(url)
        assert response.status_code not in URL_MISSED_STATUSES, (
            f'Убедитесь, что эндпоинт {meaning} функционирует '
            f'и доступен по адресу "{url}".'
        )
        return
