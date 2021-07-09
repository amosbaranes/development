from django.urls import path
from django.conf.urls import url
from .views import (home, resume)

app_name = 'portfolio'

urlpatterns = [
    path('', home, name='home'),
    url(r'^resume/(?P<pk>\d+)/$', resume, name='resume'),
]