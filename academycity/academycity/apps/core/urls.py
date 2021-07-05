
from django.urls import path
from .views import (home, update_field_model, post_ajax_create_action)

app_name = "core"

urlpatterns = [
    path('', home, name='home'),
    path('post_ajax_create_action', post_ajax_create_action, name='post_ajax_create_action'),
    path('update_field_model', update_field_model, name='update_field_model'),
]
