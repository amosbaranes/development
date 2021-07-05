from django.urls import path
from . import views

app_name = "ueconomics"

urlpatterns = [
    path(r'', views.index, name='home'),
    path(r'update_data', views.update_data, name='update_data'),
    path(r'get_source_data', views.get_source_data, name='get_source_data'),
]


