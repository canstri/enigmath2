from django.conf.urls import url
from django.contrib import admin

from .views import (
	olymps_list,
	olymp_create,
	olymp_detail,
	olymp_update,
	olymp_delete,
	)

app_name = 'Enigmath'
urlpatterns = [
	url(r'^$', olymps_list, name='list'),
    url(r'^create/$', olymp_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', olymp_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', olymp_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', olymp_delete, name='delete'),
]