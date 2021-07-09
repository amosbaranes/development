from django.conf.urls import url
from django.urls import path
from .views import home, post_contact_us, category_items

app_name = "bizland"

urlpatterns = [
    url(r'^$', home, name='home'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),
    path('pcategory_items', category_items, name='category_items'),
]
