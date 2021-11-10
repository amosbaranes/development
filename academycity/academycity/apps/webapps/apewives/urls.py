from django.conf.urls import url
from django.urls import path
from .views import home

app_name = "apewives"

urlpatterns = [
    url(r'^$', home, name='home'),
]
