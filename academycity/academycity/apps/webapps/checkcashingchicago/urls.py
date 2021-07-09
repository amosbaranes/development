from django.urls import path
from django.conf.urls import url
from .views import (home, get_location, location_detail, post_contact_us, members_area_detail,
                    post_password)

app_name = 'checkcashingchicago'

urlpatterns = [
    path('', home, name='home'),
    path('get_courses', get_location, name='get_location'),
    path('location_detail/<slug:slug>/', location_detail, name='location_detail'),
    path('members_area_detail', members_area_detail, name='members_area_detail'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),
    path('post_password', post_password, name='post_password'),
]
