# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .apps.chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from .apps.videocall.routing import websocket_urlpatterns as video_websocket_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_websocket_urlpatterns +
            video_websocket_urlpatterns
        )
    ),
})