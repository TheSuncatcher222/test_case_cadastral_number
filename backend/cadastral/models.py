from django.db import models

from backend.app_data import (
    CADASTRAL_NUMBER_LEN, CADASTRAL_NUMBER_ANY,
    HTTP_METHOD_NAME_MAX_LEN, URL_PATH_MAX_LEN,
)
from cadastral.validators import (
    validate_cadastral_number,
    validate_cadastral_lat,
    validate_cadastral_lon,
)


class CadastralNumber(models.Model):
    """Класс представления кадастрового номера."""

    number = models.CharField(
        verbose_name='Кадастровый номер',
        max_length=CADASTRAL_NUMBER_LEN,
        unique=True,
        validators=(validate_cadastral_number,),
    )
    latitude = models.FloatField(
        verbose_name='Широта (десятичные градусы)',
        validators=(validate_cadastral_lat,),
    )
    longitude = models.FloatField(
        verbose_name='Долгота (десятичные градусы)',
        validators=(validate_cadastral_lon,),
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Кадастровый номер'
        verbose_name_plural = 'Кадастровые номера'

    def __str__(self):
        return self.number


class LogsHistory(models.Model):
    """Класс представления истории запросов и ответов к серверу."""

    path = models.CharField(
        verbose_name='Путь HTTP запроса',
        max_length=URL_PATH_MAX_LEN,
    )
    method = models.CharField(
        verbose_name='Метод HTTP запроса',
        max_length=HTTP_METHOD_NAME_MAX_LEN,
    )
    request_data = models.TextField(
        verbose_name='JSON запроса',
    )
    status_code = models.IntegerField(
        verbose_name='Статус ответа',
    )
    response_data = models.TextField(
        verbose_name='JSON ответа',
    )
    # INFO: не связываю с моделью CadastralNumber, так как тут содержатся
    #       данные, указанные в HttpRequest.body, которые могут быть ошибочные.
    cadastral = models.CharField(
        verbose_name='Кадастровый номер',
        max_length=CADASTRAL_NUMBER_ANY,
    )
    datetime = models.DateTimeField(
        'Дата совершения запроса',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'HTTP запрос'
        verbose_name_plural = 'История HTTP запросов'

    def __str__(self):
        return f'{self.method} {self.path}: {self.status_code}'
