from freezegun import freeze_time
import pytest
from django.db import models

from cadastral.models import CadastralNumber, LogsHistory


def create_cadastral_obj(num: int) -> CadastralNumber:
    """Создает и возвращает объект модели CadastralNumber."""
    cadastral, _ = CadastralNumber.objects.get_or_create(
        number=f'12:12:123456:{num:02}',
        latitude=float(f'12.{num:06}'),
        longitude=float(f'12.{num:06}'),
    )
    return cadastral


def create_log_obj(num: int) -> LogsHistory:
    """Создает и возвращает объект модели LogsHistory."""
    log, _ = LogsHistory.objects.get_or_create(
        path=f'/path_{num}/',
        method=f'method_{num}',
        request_data=f'request_data_{num}',
        status_code=num,
        response_data=f'response_data_{num}',
        cadastral=f'12:12:123456:{num:02}',
    )
    return log


@pytest.mark.django_db
class TestCadastralNumberModel():
    """Производит тест модели "CadastralNumber"."""

    def test_valid_create(self) -> None:
        """Тестирует возможность создания объекта с валидными данными."""
        assert CadastralNumber.objects.all().count() == 0
        cadastral: CadastralNumber = create_cadastral_obj(num=1)
        assert CadastralNumber.objects.all().count() == 1
        assert cadastral.number == '12:12:123456:01'
        assert cadastral.latitude == 12.000001
        assert cadastral.longitude == 12.000001
        return

    def test_meta(self) -> None:
        """Тестирует мета-данные модели и полей.
        Тестирует строковое представление модели."""
        cadastral: CadastralNumber = create_cadastral_obj(num=1)
        assert str(cadastral) == '12:12:123456:01'
        assert cadastral._meta.ordering == ('-id', )
        assert cadastral._meta.verbose_name == 'Кадастровый номер'
        assert cadastral._meta.verbose_name_plural == 'Кадастровые номера'
        number = cadastral._meta.get_field('number')
        assert isinstance(number, models.CharField)
        assert number.verbose_name == 'Кадастровый номер'
        assert number.max_length == 16
        assert number.unique
        latitude = cadastral._meta.get_field('latitude')
        assert isinstance(latitude, models.FloatField)
        assert latitude.verbose_name == 'Широта (десятичные градусы)'
        longitude = cadastral._meta.get_field('longitude')
        assert isinstance(longitude, models.FloatField)
        assert longitude.verbose_name == 'Долгота (десятичные градусы)'
        status = cadastral._meta.get_field('status')
        assert isinstance(status, models.BooleanField)
        assert status.verbose_name == 'Статус'
        assert status.default is None
        assert status.blank
        assert status.null
        return


@pytest.mark.django_db
class TestLogsHistoryModel():
    """Производит тест модели "LogsHistory"."""

    @freeze_time('2000-01-01 00:00:01')
    def test_valid_create(self) -> None:
        """
        Тестирует возможность создания объекта с валидными данными.
        Так как поле datetime имеет аттрибут auto_add_now - используется
        библиотека freezegun для заморозки времени на неизменное значение.
        """
        assert LogsHistory.objects.all().count() == 0
        log: LogsHistory = create_log_obj(num=1)
        assert LogsHistory.objects.all().count() == 1
        assert log.path == '/path_1/'
        assert log.method == 'method_1'
        assert log.request_data == 'request_data_1'
        assert log.status_code == 1
        assert log.response_data == 'response_data_1'
        assert log.cadastral == '12:12:123456:01'
        assert str(log.datetime) == '2000-01-01 00:00:01+00:00'
        return

    def test_meta(self) -> None:
        """Тестирует мета-данные модели и полей.
        Тестирует строковое представление модели."""
        log: LogsHistory = create_log_obj(num=1)
        assert str(log) == 'method_1 /path_1/: 1'
        assert log._meta.ordering == ('-id', )
        assert log._meta.verbose_name == 'HTTP запрос'
        assert log._meta.verbose_name_plural == 'История HTTP запросов'
        path = log._meta.get_field('path')
        assert isinstance(path, models.CharField)
        assert path.verbose_name == 'Путь HTTP запроса'
        assert path.max_length == 255
        method = log._meta.get_field('method')
        assert isinstance(method, models.CharField)
        assert method.verbose_name == 'Метод HTTP запроса'
        assert method.max_length == 10
        request_data = log._meta.get_field('request_data')
        assert isinstance(request_data, models.TextField)
        assert request_data.verbose_name == 'JSON запроса'
        status_code = log._meta.get_field('status_code')
        assert isinstance(status_code, models.IntegerField)
        assert status_code.verbose_name == 'Статус ответа'
        response_data = log._meta.get_field('response_data')
        assert isinstance(response_data, models.TextField)
        assert response_data.verbose_name == 'JSON ответа'
        cadastral = log._meta.get_field('cadastral')
        assert isinstance(cadastral, models.CharField)
        assert cadastral.verbose_name == 'Кадастровый номер'
        assert cadastral.max_length == 255
        datetime = log._meta.get_field('datetime')
        assert isinstance(datetime, models.DateTimeField)
        assert datetime.verbose_name == 'Дата совершения запроса'
        assert datetime.auto_now_add
        return
