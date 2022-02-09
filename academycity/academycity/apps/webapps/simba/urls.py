from django.conf.urls import url
from django.urls import path
from .views import (home, candle_, candle1, candle2, candle3, candle4,
                    candle5, candle6, candle7, candle8, candle9)
app_name = "simba"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^c_$', candle_, name='candle_'),
    url(r'^c1$', candle1, name='candle1'),
    url(r'^c2$', candle2, name='candle2'),
    url(r'^c3$', candle3, name='candle3'),
    url(r'^c4$', candle4, name='candle4'),
    url(r'^c5$', candle5, name='candle5'),
    url(r'^c6$', candle6, name='candle6'),
    url(r'^c7$', candle7, name='candle7'),
    url(r'^c8$', candle8, name='candle8'),
    url(r'^c9$', candle9, name='candle9'),

]
