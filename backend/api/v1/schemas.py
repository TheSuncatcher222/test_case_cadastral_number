from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers, status

from cadastral.models import CadastralNumber
from cadastral.validators import (
    CADASTRAL_NUMBER_ERR, CADASTRAL_LAT_ERR, CADASTRAL_LON_ERR
)
from api.v1.serializers import CadastralSerializer, LogsHistorySerializer

DEFAULT_404: str = 'Страница не найдена.'


class CadastralNumberSerializer(serializers.ModelSerializer):
    """
    Вспомогательный сериализатор для POST запроса на /get_history:
    указывает необходимость указания поля 'number' в теле запроса.
    """

    class Meta:
        model = CadastralNumber
        fields = (
            'number',
        )


EXTEND_SCHEMA_CHECK_PING = extend_schema(
    summary='Проверить доступность API.',
    responses={
        status.HTTP_200_OK: None,
    },
    request=None,
)

EXTEND_SCHEMA_GET_HISTORY = extend_schema(
    summary='Получить историю обращений по кадастровому номеру.',
    responses={
        status.HTTP_200_OK: LogsHistorySerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='Cadastral data error',
            fields={
                'number': serializers.ListField(
                    default=[CADASTRAL_NUMBER_ERR],
                ),
            },
        ),
    },
    parameters=[
        CadastralNumberSerializer,
    ],
)

EXTEND_SCHEMA_GET_QUERY = extend_schema(
    summary='Записать кадастровый номер в базу данных.',
    description=(
        'Записывает кадастровый номер в базу данных и отдает его на проверку.'
    ),
    responses={
        status.HTTP_201_CREATED: CadastralSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='Cadastral data error',
            fields={
                'number': serializers.ListField(
                    default=[CADASTRAL_NUMBER_ERR],
                ),
                'latitude': serializers.ListField(
                    default=[CADASTRAL_LAT_ERR],
                ),
                'longitude': serializers.ListField(
                    default=[CADASTRAL_LON_ERR],
                ),
            },
        ),
    },
    parameters=[
        CadastralSerializer,
    ],
)

EXTEND_SCHEMA_GET_RESULT = extend_schema(
    summary='Получить статус кадастрового номера в базе данных.',
    description=(
        'Предоставляет данные указанного кадастрового номера.'
    ),
    responses={
        status.HTTP_200_OK: CadastralSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='Cadastral data error',
            fields={
                'number': serializers.ListField(
                    default=[CADASTRAL_NUMBER_ERR],
                ),
            },
        ),
        status.HTTP_404_NOT_FOUND: inline_serializer(
            name='Cadastral not found',
            fields={
                'detail': serializers.CharField(
                    default=DEFAULT_404
                ),
            },
        ),
    },
    parameters=[
        CadastralNumberSerializer,
    ],
)
