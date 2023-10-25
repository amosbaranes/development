from django.urls import path
from .views import (home, app, activate_obj_function)
from ...core.views import logmein

app_name = "mm"

urlpatterns = [
    path('', home, name='home'),
    path('logmein/', logmein, name='logmein'),
    path('app/<str:app_name>/', app, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),
]
