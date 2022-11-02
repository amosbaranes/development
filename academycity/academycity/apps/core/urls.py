
from django.urls import path
from .views import (home, app, update_field_model, post_ajax_create_action, activate_function, update_field_model_by_id,
                    get_data_link, get_data_json_link,
                    activate_obj_function
                    # , get_adjective_link
                    )

app_name = "core"

urlpatterns = [
    path('', home, name='home'),
    path('app/<str:app_name>/', app, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),

    path('post_ajax_create_action', post_ajax_create_action, name='post_ajax_create_action'),
    path('update_field_model', update_field_model, name='update_field_model'),
    path('activate_function', activate_function, name='activate_function'),
    path('update_field_model_by_id', update_field_model_by_id, name='update_field_model_by_id'),
    path('get_data_link', get_data_link, name='get_data_link'),
    path('get_data_json_link', get_data_json_link, name='get_data_json_link'),
    # path('get_adjective_link', get_adjective_link, name='get_adjective_link'),
]

