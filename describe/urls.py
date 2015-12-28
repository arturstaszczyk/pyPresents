from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
import describe
from describe import views

urlpatterns = [
    url(r'^$', views.user_page),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^logout/$', views.logout_user),

    url(r'^randomize/(?P<user_pk>[0-9]+)/$', describe.views.randomize),
]
