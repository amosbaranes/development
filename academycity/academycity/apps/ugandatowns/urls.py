from django.urls import path
from .views import (index, basic_town, menu_town, menu_town_model, post_contact_us, menu_town_other_model,
                    ut_login_page, home, create_conference, remove_conference)

app_name = 'ugandatowns'

urlpatterns = [
    # post views
    # path('', ut_login_page, name='ut_login_page'),
    path('', home, name='home'),
    path('index', index, name='index'),
    path('town/<slug:town_slug>', index, name='town'),
    path('create_conference', create_conference, name='create_conference'),
    path('remove_conference', remove_conference, name='remove_conference'),

    path('menu_town_other_model/<slug:town_slug>/<str:html>', menu_town_other_model, name='menu_town_other_model'),
    path('basic_town', basic_town, name='basic_town'),
    path('town/<slug:town_slug>/<str:menu>/<slug:item_slug>', menu_town_model, name='menu_town_model'),
    path('menu_town', menu_town, name='menu_town'),
    path('post_contact_us', post_contact_us, name='post_contact_us'),

]
