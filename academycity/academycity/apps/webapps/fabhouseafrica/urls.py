from django.urls import path
from django.conf.urls import url
from .views import (home, catalog, category, about, contact, post_contact_us, gallery, test)

app_name = 'fabhouseafrica'

urlpatterns = [
    # post views
    path('', home, name='home'),
    url(r'^(?P<pk>\d+)/$', test, name='test'),
    path('category/<int:category_id>', category, name='category'),
    path('catalog', catalog, name='catalog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('gallery', gallery, name='gallery'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),
]
