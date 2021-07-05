from django.urls import path
from django.conf.urls import url
from .views import (home, suppliers_registration)

app_name = "radiusfood"

urlpatterns = [
    path('', home, name='home'),
    url(r'^suppliers_registration/$', suppliers_registration, name='suppliers_registration'),
]


