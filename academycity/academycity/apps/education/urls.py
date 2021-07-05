from django.urls import path
from .views import (home, get_courses, get_news, get_program, get_subject, get_person)

app_name = 'education'

urlpatterns = [
    path('', home, name='home'),
    path('get_courses', get_courses, name='get_courses'),
    path('get_news', get_news, name='get_news'),
    path('get_program', get_program, name='get_program'),
    path('get_subject', get_subject, name='get_subject'),
    path('get_person', get_person, name='get_person'),
]
