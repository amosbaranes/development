from django.urls import path
from .views import (home, app, activate_obj_function, upload_file)

app_name = "avi"

urlpatterns = [
    path('', home, name='home'),
    path('app/<str:app_name>/', app, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),
    path('upload_file/', upload_file, name='upload_file'),
]
