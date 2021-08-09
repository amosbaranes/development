from django.urls import path
from django.conf.urls import url
from .views import (home, resume, test, service)

app_name = 'portfolio'

urlpatterns = [
    path('', home, name='home'),
    url(r'^(?P<pk>\d+)/$', test, name='test'),
    url(r'^service/(?P<pk>\d+)/$', service, name='service'),
    url(r'^resume/(?P<pk>\d+)/$', resume, name='resume'),
]