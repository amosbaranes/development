from django.urls import path
from .views import index, save_data, get_data, get_user_swot, delete_data

app_name = "swotclock"

urlpatterns = [
    path('', index, name='index'),
    path('save_data', save_data, name='save_data'),
    path('get_data', get_data, name='get_data'),
    path('get_user_swot', get_user_swot, name='get_user_swot'),
    path('delete_data', delete_data, name='delete_data'),
]

