from django.conf.urls import url
from django.contrib import admin

from .views import (
    problem_thread,
    problem_delete

    )

app_name = 'Enigmath_problems'
urlpatterns = [
    url(r'^(?P<id>\d+)/$', problem_thread, name='thread'),
    url(r'^(?P<id>\d+)/delete/$', problem_delete, name='delete'),
]