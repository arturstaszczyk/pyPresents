from django.conf.urls import *
from django.contrib import admin
import describe
from describe import urls

urlpatterns =[
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(describe.urls)),
]
