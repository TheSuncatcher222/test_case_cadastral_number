from django.contrib import admin

from backend.app_data import ADMIN_LIST_PER_PAGE
from cadastral.models import CadastralNumber


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
