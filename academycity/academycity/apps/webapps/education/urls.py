from django.urls import path
from django.conf.urls import url
from .views import (home, get_courses, get_news, get_program, get_subject, get_person,
                    course_description, news_detail, program_description, subject_description,
                    login_page, signup_page)

app_name = 'education'

urlpatterns = [
    path('', home, name='home'),
    path('get_courses', get_courses, name='get_courses'),
    path('get_news', get_news, name='get_news'),
    path('get_program', get_program, name='get_program'),
    path('get_subject', get_subject, name='get_subject'),
    path('get_person', get_person, name='get_person'),
    path('news_detail', news_detail, name='news_detail'),
    url(r'^course_description/(?P<pk>\d+)/$', course_description, name='course_description'),
    url(r'^program_description/(?P<pk>\d+)/$', program_description, name='program_description'),
    url(r'^subject_description/(?P<pk>\d+)/$', subject_description, name='subject_description'),

    path('login_page', login_page, name='login_page'),
    path('signup_page', signup_page, name='signup_page'),
]