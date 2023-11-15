import requests

from celery import shared_task, group
from django.db.models import QuerySet

from backend.app_data import EXTERNAL_SERVER_URL
from backend.settings import CHUNK_CELERY
from cadastral.models import CadastralNumber


def http_post_request_to_validate(cadastral: CadastralNumber) -> str | None:
    """
    Производит POST запрос на сервер валидации кадастровых номеров.
    Возвращает статус кадастрового номера.
    Если статус отсутствует в теле ответа, или он не является bool-типа,
    возвращает None.
    """
    data: dict[str, any] = {
        'number': cadastral.number,
        'latitude': cadastral.latitude,
        'longitude': cadastral.longitude,
    }
    headers: dict[str, str] = {
        'Content-Type': 'application/json',
    }
    response: requests = requests.post(
        url=EXTERNAL_SERVER_URL,
        json=data,
        headers=headers,
    )
    status: str = response.json().get('status')
    if status not in (True, False):
        return None
    return status


@shared_task
def validate_cadastral_groups(cadastral_group: list[int]) -> None:
    # INFO: Celery использует формат JSON для передачи данных в брокер.
    #       Ввиду того, что сообщений предполагается не очень большое
    #       количество даже на прод-сервере, было решено упростить код
    #       для читаемости и совершать вторичные обращения к БД.
    cadastral_group: QuerySet = CadastralNumber.objects.filter(
        id__in=cadastral_group,
    )
    for cadastral in cadastral_group:
        status: str = http_post_request_to_validate(cadastral=cadastral)
        if status is not None:
            cadastral.status = status
    CadastralNumber.objects.bulk_update(
        objs=list(cadastral_group),
        fields=('status',),
    )
    return


@shared_task
def validate_cadastral_numbers() -> None:
    """
    Celery задача отправки запроса на сервер валидации кадастровых номеров.

    Выбирает из базы данных кадастровые номера без подтвержденного статуса,
    разбивает из на группы по CHUNK штук, ставит в очередь задачу(и)
    validate_cadastral_groups для отправки запроса на сервер валидации.
    """
    no_status_cadastral_ids: list[int] = (
        CadastralNumber.objects.filter(
            status=None,
        ).values_list(
            'id',
            flat=True,
        )
    )
    if not no_status_cadastral_ids:
        return
    cadastral_groups: list[int] = [
        no_status_cadastral_ids[i:(i+CHUNK_CELERY)] for
        i in range(0, len(no_status_cadastral_ids), CHUNK_CELERY)
    ]
    celery_group: group = group(
        validate_cadastral_groups.s(cadastral_group=cadastral_group) for
        cadastral_group in cadastral_groups
    )
    celery_group.apply_async()
    return
