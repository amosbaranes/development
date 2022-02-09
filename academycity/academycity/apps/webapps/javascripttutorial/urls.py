from django.conf.urls import url
from django.urls import path
from .views import home, motion, whiteboard, lists, tab, data_tab, add_tab, delete_tab, get_tabs_from_table, update_text_tab
app_name = "javascripttutorial"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^m$', motion, name='motion'),
    url(r'^l$', lists, name='lists'),
    url(r'^t$', tab, name='tab'),
    url(r'^d$', data_tab, name='data_tab'),
    url(r'^w$', whiteboard, name='whiteboard'),
    url(r'^add_tab$', add_tab, name='add_tab'),
    url(r'^delete_tab$', delete_tab, name='delete_tab'),
    url(r'^update_text_tab$', update_text_tab, name='update_text_tab'),
    url(r'^get_tabs_from_table$', get_tabs_from_table, name='get_tabs_from_table'),

]
