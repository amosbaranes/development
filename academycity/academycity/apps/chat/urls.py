from django.urls import path, re_path
from .views import (index, get_or_create_wb, get_wb_of_section)

app_name = "chat"

urlpatterns = [
    # path('', index, name='index'),
    path('wb/get_or_create_wb', get_or_create_wb, name='get_or_create_wb'),
    path('wb/get_wb_of_section', get_wb_of_section, name='get_wb_of_section'),
    re_path(r"^(?P<username>[\w.@+-]+)", index, name='index'),
]
