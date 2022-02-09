#-*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (IndexView, DetailView, ResultsView, ResultsAll, vote, vote_all, samuel)

app_name = "polls"

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', ResultsView.as_view(), name='results'),
    url(r'^results_all/$', ResultsAll.as_view(), name='results_all'),
    url(r'^(?P<poll_id>\d+)/vote/$', vote, name='vote'),
    url(r'^vote_all/$', vote_all, name='vote_all'),

    url(r'^samuel/$', samuel, name='samuel'),

]
