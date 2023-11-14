from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.app_data import RESPONSE_DATA_API_AVAILABLE


@api_view(http_method_names=('POST',))
def check_ping(request):
    return Response(data=RESPONSE_DATA_API_AVAILABLE, status=HTTP_200_OK)
