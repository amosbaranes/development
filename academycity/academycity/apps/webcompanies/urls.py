
from django.urls import path
from .views import (home)

app_name = "webcompanies"

urlpatterns = [
    path('', home, name='home'),
]
