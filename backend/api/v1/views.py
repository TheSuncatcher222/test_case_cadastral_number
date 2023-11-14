from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.v1.serializers import CadastralSerializer
from backend.app_data import RESPONSE_DATA_API_AVAILABLE
from cadastral.models import CadastralNumber
from cadastral.validators import validate_cadastral_number


@api_view(http_method_names=('POST',))
def check_ping(request):
    """Возвращает статус 200, если сервер успешно функционирует."""
    return Response(data=RESPONSE_DATA_API_AVAILABLE, status=HTTP_200_OK)


@api_view(http_method_names=('POST',))
def get_query(request):
    """
    Создает запись в БД для модели CadastralNumber.
    Создает задачу для Celery проверить статус созданного кадастрового номера.
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
    # TODO: добавить задачу для Celery отправить запрос на проверку статуса.
    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(http_method_names=('GET',))
def get_result(request):
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
            status=HTTP_400_BAD_REQUEST,
        )
    cadastral: CadastralNumber = get_object_or_404(
        CadastralNumber,
        number=number,
    )
    serializer: Serializer = CadastralSerializer(instance=cadastral)
    return Response(
        data=serializer.data,
        status=HTTP_200_OK,
    )
