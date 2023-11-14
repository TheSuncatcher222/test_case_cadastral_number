from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.v1.serializers import CadastralSerializer
from backend.app_data import RESPONSE_DATA_API_AVAILABLE


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
    serializer: Serializer = CadastralSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # TODO: добавить задачу для Celery отправить запрос на проверку статуса.
    return Response(data=serializer.data, status=HTTP_200_OK)
