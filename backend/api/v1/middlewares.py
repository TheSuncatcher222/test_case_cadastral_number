import json

from django.utils.deprecation import MiddlewareMixin

from backend.app_data import PATH_QUERY, PATH_RESULT
from cadastral.models import LogsHistory


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Определяет механизм обработки запросов и ответов:
    сохраняет историю запросов и ответов на сервер в базу данных.
    """

    def process_response(self, request, response):
        """
        Сохраняет данные запроса от ответа
        перед конечной отправкой ответа клиенту.
        """
        if request.path not in (PATH_QUERY, PATH_RESULT):
            return response
        # INFO: согласно официальной документации:
        #       https://docs.djangoproject.com/en/4.2/ref/request-response/#httprequest-objects  # noqa(E303)
        #       The raw HTTP request body as a bytestring.
        #       То есть на надо сериализировать эти данные
        #       в текстовый объект для models.Textfield поля.
        request_data: dict = request._cached_body
        cadastral: str = request_data.get('number', None)
        log_entry = LogsHistory(
            path=request.path,
            method=request.method,
            request_data=json.dumps(request_data),
            status_code=response.status_code,
            response_data=json.dumps(
                response.content.decode('utf-8'),
                ensure_ascii=False
            ),
            cadastral=cadastral,
        )
        log_entry.save()
        return response
