from django.urls import path
from django.conf.urls import url
from .views import (instructors, instructor_tag)

app_name = "instructors"

urlpatterns = [
    path('instructors/<slug:slug>/', instructors, name='instructor'),
    path('instructor_tag/<slug:slug>/', instructor_tag, name='instructor_tag'),
]

