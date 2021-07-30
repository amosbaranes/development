from django.conf.urls import url
from django.urls import path
from .views import home, post_contact_us, category_items, test

app_name = "bizland"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^(?P<pk>\d+)/$', test, name='test'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),
    path('pcategory_items', category_items, name='category_items'),
]
