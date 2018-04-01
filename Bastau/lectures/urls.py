from django.conf.urls import url
from django.contrib import admin

from .views import (
    lecture_detail,
    lecture_delete,
    )

app_name = 'Enigmath'
urlpatterns = [
    url(r'^(?P<id>[\w-]+)/$', lecture_detail, name='detail'),
    url(r'^(?P<id>[\w-]+)/delete/$', lecture_delete, name='delete'),
]