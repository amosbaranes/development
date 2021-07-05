from django.urls import path
from .views import (home, get_screens,
                    management, link_management_data,
                    team, get_sub_screens, get_or_create_product,
                    update_attribute_value, change_segment, change_game_types, change_randd,
                    update_abandon_product)

app_name = "globsim"

urlpatterns = [
    path('home/<int:obj_id>/', home, name='home'),

    path('get_screens', get_screens, name='get_screens'),
    path('get_sub_screens', get_sub_screens, name='get_sub_screens'),
    path('get_or_create_product', get_or_create_product, name='get_or_create_product'),

    path('update_attribute_value', update_attribute_value, name='update_attribute_value'),
    path('change_segment', change_segment, name='change_segment'),
    path('change_game_types', change_game_types, name='change_game_types'),

    path('change_randd', change_randd, name='change_randd'),
    path('management/', management, name='management'),
    path('link_management_data/', link_management_data, name='link_management_data'),

    path('team/', team, name='team'),
    path('update_abandon_product/', update_abandon_product, name='update_abandon_product'),

]


