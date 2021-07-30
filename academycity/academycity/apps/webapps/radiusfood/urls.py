from django.urls import path
from django.conf.urls import url
from .views import (home, suppliers_registration, test)

app_name = "radiusfood"

urlpatterns = [
    path('', home, name='home'),
    url(r'^(?P<pk>\d+)/$', test, name='test'),
    url(r'^suppliers_registration/$', suppliers_registration, name='suppliers_registration'),
]


