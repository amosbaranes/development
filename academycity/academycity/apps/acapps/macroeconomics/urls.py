from django.conf.urls import url
from .views import (home)

app_name = "macroeconomics"

urlpatterns = [
    url(r'^$', home, name='home'),
]
