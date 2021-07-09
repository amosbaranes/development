from django.conf.urls import url
from django.contrib.auth.views import (LoginView, LogoutView,)
from .views import (home)

app_name = "trading"

urlpatterns = [
    url(r'^$', home, name='home'),
]
