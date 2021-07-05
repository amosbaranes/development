from django.urls import path
from .views import (home, currency_exchange, get_option_chain, run_options_engine, option_trading)
from .simview import sim_home

app_name = "trades"

urlpatterns = [
    path('sim_home/', sim_home, name='sim_home'),
    path('currency_exchange', currency_exchange, name='currency_exchange'),
    path('currency_exchange/<currencies>', currency_exchange, name='currency_exchange_wc'),

    path('get_option_chain', get_option_chain, name='get_option_chain'),
    path('run_options_engine', run_options_engine, name='run_options_engine'),

    path('option_trading', option_trading, name='option_trading'),
    path('', home, name='home'),
]
