from django.urls import path
from django.conf.urls import url
from .views import (home, partner_detail, instructors, instructor_tag)

app_name = "partners"

urlpatterns = [
    path('', home, name='home'),
    path('instructors/', instructors, name='instructors'),
    path('partner_detail/<slug:slug>/', partner_detail, name='partner_detail'),
]

