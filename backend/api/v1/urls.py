from django.urls import path

from api.v1.views import get_history, get_result, get_query, check_ping

urlpatterns = [
    path(route='ping/', view=check_ping),
    path(route='history/', view=get_history),
    path(route='result/', view=get_result),
    path(route='query/', view=get_query),
]
