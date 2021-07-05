from django.urls import path
from .views import (product_list, product_detail)

app_name = "shop"

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product_detail/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
]

# need to add edit

