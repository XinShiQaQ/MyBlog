from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('Login', views.get_admin_login_page),
    path('LoginResult', views.check_login),
    path('', views.get_admin_page),
    path('quit', views.quits),
    re_path(r'modifyArticles/(.*)', views.get_modify_article_page),
    re_path(r'modifyConfirm/(.*)', views.modify_confirm),
    re_path(r'deleteArticle/(.*)', views.delete_article),
    path('modifyCategory', views.get_modify_category_page)
]
