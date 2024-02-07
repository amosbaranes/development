from django.urls import path
from .views import (home, app, activate_obj_function, myfirstwebpage, basic)

app_name = "kiu"

urlpatterns = [
    path('', home, name='home'),
    path('app/<str:app_name>/', app, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),
    path('myfirstwebpage/', myfirstwebpage, name='myfirstwebpage'),
    path('basic/', basic, name='basic'),
]
