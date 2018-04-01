"""Enigmath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from accounts.views import (login_view, register_view, logout_view)
from main.views import(main_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^news/', include("news.urls", namespace='news')),
    url(r'^profile/', include("accounts.urls", namespace='accounts')),
    url(r'^olympiads/', include("olymps.urls", namespace='olymps')),
    url(r'^problems/', include("problems.urls", namespace='problems')),
    url(r'^courses/', include("courses.urls", namespace='courses')),
    url(r'^lectures/', include("lectures.urls", namespace='lectures')),
    url(r'^', include("main.urls", namespace='main')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

