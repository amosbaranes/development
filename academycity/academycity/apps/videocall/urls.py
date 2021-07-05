from django.urls import path
# from .views import VideoCall
from .views import video_call, video_simple

app_name = "videocall"

urlpatterns = [
    # path('video_call/', VideoCall.as_view(), name='video_call'),
    path('video_call/', video_call, name='video_call'),
    path('video_simple/', video_simple, name='_simple'),
]