from django.contrib import admin
from django.urls import path, re_path,include
from . import views

urlpatterns = [
    path('', views.get_home_page),
    re_path(r'^([^/]*)/$', views.get_home_page)
]
