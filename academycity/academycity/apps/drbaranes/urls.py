from django.urls import path
from .views import index

app_name = 'drbaranes'

urlpatterns = [
    # post views
    path('', index, name='index'),
]
