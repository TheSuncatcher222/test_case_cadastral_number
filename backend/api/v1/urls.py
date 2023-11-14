from django.urls import path

from api.v1.views import check_ping

urlpatterns = [
    path(route='ping/', view=check_ping),
]
