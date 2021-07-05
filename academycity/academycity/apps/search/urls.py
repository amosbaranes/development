
from django.urls import path
from .views import (home, search)

app_name = "search"

urlpatterns = [
    path('', home, name='home'),
    path('search', search, name='search'),
]
