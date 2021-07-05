
from django.urls import path
from .views import (home)

app_name = "actions"

urlpatterns = [
    path('', home, name='home'),
]
