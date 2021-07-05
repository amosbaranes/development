from django.urls import path
from .views import (potential)

app_name = "research"

urlpatterns = [
    path('potential', potential, name='potential'),
]
