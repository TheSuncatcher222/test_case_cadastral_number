from django.contrib import admin

from backend.app_data import ADMIN_LIST_PER_PAGE
from cadastral.models import CadastralNumber, LogsHistory


@admin.register(CadastralNumber)
class CadastralNumberAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django
    для модели CadastralNumber.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - id (id)
            - кадастровый номер (number)
            - широта в десятичных градусах (latitude)
            - долгота в десятичных градусах (longitude)
            - статус номера (status)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - кадастровый номер (number)
            - широта в десятичных градусах (latitude)
            - долгота в десятичных градусах (longitude)
            - статус номера (status)
        - list_filter (tuple) - список фильтров:
            - статус номера (status)
        - search_fields (tuple) - список полей для поиска объектов:
            - кадастровый номер (number)
            - широта в десятичных градусах (latitude)
            - долгота в десятичных градусах (longitude)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'number',
        'latitude',
        'longitude',
        'status',
    )
    list_editable = (
        'number',
        'latitude',
        'longitude',
        'status',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'number',
        'latitude',
        'longitude',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(LogsHistory)
class LogsHistoryAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django
    для модели LogsHistory.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - id (id)
            - путь HTTP запроса (path)
            - метод HTTP запроса (method)
            - JSON запроса (request_data)
            - статус ответа (status_code)
            - JSON ответа (response_data)
            - кадастровый номер (cadastral)
            - дата и время запроса (datetime)
        - list_filter (tuple) - список фильтров:
            - путь HTTP запроса (path)
            - метод HTTP запроса (method)
            - статус ответа (status_code)
        - search_fields (tuple) - список полей для поиска объектов:
            - дата и время запроса (datetime)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'path',
        'method',
        'request_data',
        'status_code',
        'response_data',
        'cadastral',
        'datetime',
    )
    list_filter = (
        'path',
        'method',
        'status_code',
        'cadastral',
    )
    search_fields = (
        'datetime',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
