# chat/routing.py
from django.urls import path

from .consumers import VideoCallSignalConsumer

websocket_urlpatterns = [
    path(r'ws/video_call/signal/', VideoCallSignalConsumer),
]