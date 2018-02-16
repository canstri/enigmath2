from django.conf.urls import url
from django.contrib import admin

from .views import (
    course_list,
    )

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', course_list, name='list'),
]