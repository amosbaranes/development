# chat/routing.py
from django.urls import re_path, path
from django.conf.urls import url

from .consumers import ChatWhiteBaordConsumer, OptionsConsumer
    # ChatConsumer

websocket_urlpatterns = [
    # path("chat/<username>/", ChatConsumer),        #not working
    # url(r'^chat/(?P<usernam>[\w.@+-]+)/$', ChatConsumer),        #not working

    # url(r'ws/chat/(?P<group>\w+)/$', ChatConsumer),
    url(r'ws/chat/(?P<group>\w+)/$', ChatWhiteBaordConsumer),
    url(r'ws/option/(?P<group>\w+)/$', OptionsConsumer),
]
