# chat/routing.py
from django.urls import re_path, path
from django.conf.urls import url

from .consumers_todelete import OptionsConsumer

websocket_urlpatterns = [
    url(r'ws/option/(?P<group>\w+)/$', OptionsConsumer),
]

