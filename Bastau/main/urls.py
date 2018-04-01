from django.conf.urls import url
from django.contrib import admin

from .views import (
    main_view,
    contacts_view,
    )

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^contacts/$', contacts_view, name='contacts'),
]