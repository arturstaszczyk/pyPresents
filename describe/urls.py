from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Xmass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.main_page),
    url(r'^accounts/login/$', auth_views.login),
)
