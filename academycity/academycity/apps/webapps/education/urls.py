from django.urls import path
from django.conf.urls import url
from .views import (home, course_description, news_detail, program_description, subject_description,
                    service_description, news_description, additional_topics)

app_name = 'education'

urlpatterns = [
    path('', home, name='home'),
    path('news_detail', news_detail, name='news_detail'),
    url(r'^course_description/(?P<pk>\d+)/$', course_description, name='course_description'),
    url(r'^program_description/(?P<pk>\d+)/$', program_description, name='program_description'),
    url(r'^subject_description/(?P<pk>\d+)/$', subject_description, name='subject_description'),
    url(r'^service_description/(?P<pk>\d+)/$', service_description, name='service_description'),
    url(r'^additional_topics/(?P<pk>\d+)/$', additional_topics, name='additional_topics'),
    url(r'^news_description/(?P<pk>\d+)/$', news_description, name='news_description'),
]
