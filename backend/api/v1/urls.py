from django.urls import path

from api.v1.views import get_query, check_ping

urlpatterns = [
    path(route='ping/', view=check_ping),
    path(route='query/', view=get_query),
]
