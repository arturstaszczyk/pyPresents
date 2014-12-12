from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = patterns('',

    url(r'^$', views.user_page),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^logout/$', views.logout_user),
)
