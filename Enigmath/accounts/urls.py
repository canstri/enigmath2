from django.conf.urls import url
from django.contrib import admin

from .views import (
	account_view,
	)
from django.contrib.auth.models import User

app_name = 'accounts'
urlpatterns = [
    url(r'^(?P<user>[\w-]+)/$', account_view, name='profile'),
#    url(r'^(?P<slug>[\w-]+)/edit/$', news_update, name='update'),
#    url(r'^(?P<slug>[\w-]+)/delete/$', news_delete, name='delete'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]