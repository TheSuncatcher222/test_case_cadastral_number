from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.v1.serializers import CadastralSerializer, LogsHistorySerializer
from api.v1.schemas import (
    EXTEND_SCHEMA_CHECK_PING, EXTEND_SCHEMA_GET_HISTORY,
    EXTEND_SCHEMA_GET_QUERY, EXTEND_SCHEMA_GET_RESULT,
)
from backend.app_data import RESPONSE_DATA_API_AVAILABLE
from cadastral.models import CadastralNumber, LogsHistory
from cadastral.validators import validate_cadastral_number


@EXTEND_SCHEMA_CHECK_PING
@api_view(http_method_names=('POST',))
def check_ping(request) -> Response:
    """Возвращает статус 200, если сервер успешно функционирует."""
    return Response(
        data=RESPONSE_DATA_API_AVAILABLE,
        status=status.HTTP_200_OK,
    )


@EXTEND_SCHEMA_GET_HISTORY
@api_view(http_method_names=('GET',))
def get_history(request) -> Response:
    """
    Предоставляет историю запросов по указанному кадастровому номеру:
        - дата запроса
        - данные запроса
        - статус ответа
        - данные ответа
    """
    number: str = request.data.get('number', '')
    try:
        validate_cadastral_number(value=number)
    except ValidationError as err:
        return Response(
            data={'number': err},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # TODO: добавить пагинатор.
    logs: QuerySet = LogsHistory.objects.filter(cadastral=number)
    serializer: Serializer = LogsHistorySerializer(instance=logs, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@EXTEND_SCHEMA_GET_QUERY
@api_view(http_method_names=('POST',))
def get_query(request) -> Response:
    """
    Создает запись в БД для модели CadastralNumber.
    """
    # INFO: Согласно официальной документации:
    #       https://docs.djangoproject.com/en/4.2/ref/request-response/#httprequest-objects  # noqa(E303)
    #       данные хранятся в атрибуте "body", однако доступ к этому аттрибуту
    #       "однаразовый". При повторном обращении к request.body в
    #       RequestLoggingMiddleware возникнет следующая ошибка:
    #           raise RawPostDataException(
    #               django.http.request.RawPostDataException: You cannot access
    #               body after reading from request's data stream
    #       Таким образом появилась необходимость закешировать данные
    #       в другом аттрибуте объекта httprequest.
    #       Костыль, не спорю. Но я не нашел пока способа с этим разобраться.
    request_data: dict = request.data
    setattr(request._request, '_cached_body', request_data)
    serializer: Serializer = CadastralSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED,
    )


@EXTEND_SCHEMA_GET_RESULT
@api_view(http_method_names=('GET',))
def get_result(request) -> Response:
    """
    Возвращает данные по сообщенному кадастровому номеру.
    """
    # INFO: написал логику самостоятельно ввиду того, что если создавать
    #       сериализатор и проверять number через него - будет два обращения
    #       к базе данных: на этапе валидации, на этапе обращения к объекту.
    # INFO: про _cached_body см. INFO в get_query выше.
    request_data: dict = request.data
    setattr(request._request, '_cached_body', request_data)
    number: str = request_data.get('number', '')
    try:
        validate_cadastral_number(value=number)
    except ValidationError as err:
        return Response(
            data={'number': err},
            status=status.HTTP_400_BAD_REQUEST,
        )
    cadastral: CadastralNumber = get_object_or_404(
        CadastralNumber,
        number=number,
    )
    serializer: Serializer = CadastralSerializer(instance=cadastral)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK,
    )
