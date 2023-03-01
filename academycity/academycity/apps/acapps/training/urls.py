from django.urls import path
from .views import (home,
                    # homet, home_logged,
                    app, appt, app_id, activate_obj_function)
from ...core.views import logmein

app_name = "training"

urlpatterns = [
    path('', home, name='home'),
    path('logmein/', logmein, name='logmein'),
    # path('appt/', homet, name='homet'),
    # path('home_logged/', home_logged, name='home_logged'),
    path('appt/<str:app_name>/', appt, name='appt'),
    path('app/<str:app_name>/', app, name='app'),
    path('app/<str:app_name>/<int:company_obj_id>/', app_id, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),
]