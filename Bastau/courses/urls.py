from django.conf.urls import url
from django.contrib import admin

from .views import (
    course_list,
    course_create,
    course_detail,
    course_update,
    course_delete,
    )

app_name = 'Bastau'
urlpatterns = [
    url(r'^$', course_list, name='list'),
    url(r'^create/$', course_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', course_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', course_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', course_delete, name='delete'),
]