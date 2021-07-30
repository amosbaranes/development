from django.urls import path
from django.conf.urls import url
from .views import (home, location_detail, post_contact_us, members_area_detail,
                    post_password, test)

app_name = 'checkcashingchicago'

urlpatterns = [
    path('', home, name='home'),
    url(r'^(?P<pk>\d+)/$', test, name='test'),
    path('location_detail/<slug:slug>/', location_detail, name='location_detail'),
    path('members_area_detail', members_area_detail, name='members_area_detail'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),
    path('post_password', post_password, name='post_password'),
]
