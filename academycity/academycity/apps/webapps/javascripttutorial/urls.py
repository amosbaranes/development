from django.conf.urls import url
from django.urls import path
from .views import (home, motion, whiteboard, lists, tab, data_tab)

app_name = "javascripttutorial"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^m/', motion, name='motion'),
    url(r'^l/', lists, name='lists'),
    url(r'^t/', tab, name='tab'),
    url(r'^d/', data_tab, name='data_tab'),
    url(r'^w/', whiteboard, name='whiteboard'),
]
