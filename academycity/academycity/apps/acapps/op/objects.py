import math
import warnings
import os

import numpy
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
import matplotlib.pyplot as plt

from openpyxl import Workbook, load_workbook

import sklearn
from sklearn.datasets import make_circles

from sklearn import linear_model, neighbors
from sklearn import preprocessing
from sklearn import pipeline
import tarfile
import zipfile
from six.moves import urllib
import hashlib
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
import matplotlib.image as mpimg
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import cross_val_score
from scipy import stats
import joblib

from datetime import datetime, timedelta

"""
 to_data_path_ is the place datasets are kept
 topic_id name of the chapter to store images
"""

import pandas as pd
import numpy as np
from scipy.stats import norm

import math

#
from .objects_extensions.options import BinomialEuropeanOption, OptionDataProcessing, MLAT
from .objects_extensions.strategy import StrategyDataProcessing
#
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from django.apps import apps
# ---
import yfinance as yf
import quandl
from scipy import stats
from alpha_vantage.timeseries import TimeSeries

from abc import ABC, abstractmethod
import v20

# ----
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
from copy import deepcopy

# import seaborn as sns
# ---
# import talib
# ---


#
# ======================================
class Broker(object):
    # print("CC1 OandaBroker")
    def __init__(self, dic):
        # print("CC5 OandaBroker\n", "-"*100, "\n", dic, "\n", "-"*100)
        self.host = dic["host"]
        self.port = dic["port"]
        self.__price_event_handler = None
        self.__order_event_handler = None
        self.__position_event_handler = None

    @property
    def on_price_event(self):
        """
        Listeners will receive:
        symbol, bid, ask
        """
        return self.__price_event_handler

    @on_price_event.setter
    def on_price_event(self, event_handler):
        self.__price_event_handler = event_handler

    @property
    def on_order_event(self):
        """
        Listeners will receive:
        transaction_id
        """
        return self.__order_event_handler

    @on_order_event.setter
    def on_order_event(self, event_handler):
        self.__order_event_handler = event_handler

    @property
    def on_position_event(self):
        """
        Listeners will receive:
        symbol, is_long, units, unrealized_pnl, pnl
        """
        return self.__position_event_handler

    @on_position_event.setter
    def on_position_event(self, event_handler):
        self.__position_event_handler = event_handler

    @abstractmethod
    def get_prices(self, symbols=[]):
        """
        Query market prices from a broker
        :param symbols: list of symbols recognized by your broker
        """
        raise NotImplementedError('Method is required!')

    @abstractmethod
    def stream_prices(self, symbols=[]):
        """"
        Continuously stream prices from a broker.
        :param symbols: list of symbols recognized by your broker
        """
        raise NotImplementedError('Method is required!')

    @abstractmethod
    def send_market_order(self, symbol, quantity, is_buy):
        raise NotImplementedError('Method is required!')


class OandaBroker(Broker):
    # print("AA OandaBroker")
    PRACTICE_API_HOST = 'api-fxpractice.oanda.com'
    PRACTICE_STREAM_HOST = 'stream-fxpractice.oanda.com'

    LIVE_API_HOST = 'api-fxtrade.oanda.com'
    LIVE_STREAM_HOST = 'stream-fxtrade.oanda.com'

    PORT = '443'

    def __init__(self, dic):
        # print("AA  OandaBroker\n", "-"*100, "\n", dic, "\n", "-"*100)
        # super().__init__(dic)
        super(OandaBroker, self).__init__(dic)

        accountid = dic["accountid"]
        token = dic["token"]
        is_live = eval(dic["is_live"]) # False
        if is_live:
            host = self.LIVE_API_HOST
            stream_host = self.LIVE_STREAM_HOST
        else:
            host = self.PRACTICE_API_HOST
            stream_host = self.PRACTICE_STREAM_HOST
        # print("AA3 OandaBroker")

        self.accountid = accountid
        self.token = token

        try:
            self.api = v20.Context(host, self.port, token=token)
        except Exception as ex:
            print("Error 80-100-1", ex)
        try:
            self.stream_api = v20.Context(stream_host, self.port, token=token)
        except Exception as ex:
            print("Error 80-100-2", ex)

    def test(self, dic):
        print(" 90-100-1 OandaBroker.test\n", "-"*100, "\n", dic, "\n", "-"*100)

        result = {"status": "ok"}
        # print(result)
        return result
# ======================================

# -- Mastering Python for Finance --
# ========== Chapter 9 ============================

# ==============================================
#     def get_prices(self, symbols=[]):
#         response = self.api.pricing.get(
#             self.accountid,
#             instruments=",".join(symbols),
#             snapshot=True,
#             includeUnitsAvailable=False
#         )
#         body = response.body
#         prices = body.get('prices', [])
#         for price in prices:
#             self.process_price(price)
#
#     def process_price(self, price):
#         symbol = price.instrument
#
#         if not symbol:
#             print('Price symbol is empty!')
#             return
#
#         bids = price.bids or []
#         price_bucket_bid = bids[0] if bids and len(bids) > 0 else None
#         bid = price_bucket_bid.price if price_bucket_bid else 0
#
#         asks = price.asks or []
#         price_bucket_ask = asks[0] if asks and len(asks) > 0 else None
#         ask = price_bucket_ask.price if price_bucket_ask else 0
#
#         self.on_price_event(symbol, bid, ask)
#
#     def stream_prices(self, symbols=[]):
#         response = self.stream_api.pricing.stream(
#             self.accountid,
#             instruments=",".join(symbols),
#             snapshot=True
#         )
#
#         for msg_type, msg in response.parts():
#             if msg_type == "pricing.Heartbeat":
#                 continue
#             elif msg_type == "pricing.ClientPrice":
#                 self.process_price(msg)
#
#     def send_market_order(self, symbol, quantity, is_buy):
#         response = self.api.order.market(
#             self.accountid,
#             units=abs(quantity) * (1 if is_buy else -1),
#             instrument=symbol,
#             type='MARKET',
#         )
#         if response.status != 201:
#             self.on_order_event(symbol, quantity, is_buy, None, 'NOT_FILLED')
#             return
#
#         body = response.body
#         if 'orderCancelTransaction' in body:
#             self.on_order_event(symbol, quantity, is_buy, None, 'NOT_FILLED')
#             return
#
#         transaction_id = body.get('lastTransactionID', None)
#         self.on_order_event(symbol, quantity, is_buy, transaction_id, 'FILLED')
#
#     def get_positions(self):
#         response = self.api.position.list(self.accountid)
#         body = response.body
#         positions = body.get('positions', [])
#         for position in positions:
#             symbol = position.instrument
#             unrealized_pnl = position.unrealizedPL
#             pnl = position.pl
#             long = position.long
#             short = position.short
#
#             if short.units:
#                 self.on_position_event(
#                     symbol, False, short.units, unrealized_pnl, pnl)
#             elif long.units:
#                 self.on_position_event(
#                     symbol, True, long.units, unrealized_pnl, pnl)
#             else:
#                 self.on_position_event(
#                     symbol, None, 0, unrealized_pnl, pnl)
#
# ACCOUNT_ID = '101-001-1374173-001'
# API_TOKEN = '6ecf6b053262c590b78bb8199b85aa2f-d99c54aecb2d5b4583a9f707636e8009'
#
# broker = OandaBroker(ACCOUNT_ID, API_TOKEN)
# SYMBOL = 'EUR_USD'
#
# def on_price_event(symbol, bid, ask):
#     print(
#         datetime.now(), '[PRICE]',
#         symbol, 'bid:', bid, 'ask:', ask
#     )
#
#
# broker.on_price_event = on_price_event
# broker.get_prices(symbols=[SYMBOL])
#
# def on_order_event(symbol, quantity, is_buy, transaction_id, status):
#     print(
#         datetime.now(), '[ORDER]',
#         'transaction_id:', transaction_id,
#         'status:', status,
#         'symbol:', symbol,
#         'quantity:', quantity,
#         'is_buy:', is_buy,
#     )
#
#
# broker.on_order_event = on_order_event
# broker.send_market_order(SYMBOL, 1, True)
#
# def on_position_event(symbol, is_long, units, upnl, pnl):
#     print(
#         datetime.now(), '[POSITION]',
#         'symbol:', symbol,
#         'is_long:', is_long,
#         'units:', units,
#         'upnl:', upnl,
#         'pnl:', pnl
#     )
#
#
# broker.on_position_event = on_position_event
# broker.get_positions()
#
#
# class MeanReversionTrader(object):
#     def __init__(
#             self, broker, symbol=None, units=1,
#             resample_interval='60s', mean_periods=5
#     ):
#         """
#         A trading platform that trades on one side
#             based on a mean-reverting algorithm.
#
#         :param broker: Broker object
#         :param symbol: A str object recognized by the broker for trading
#         :param units: Number of units to trade
#         :param resample_interval:
#             Frequency for resampling price time series
#         :param mean_periods: Number of resampled intervals
#             for calculating the average price
#         """
#         self.broker = self.setup_broker(broker)
#
#         self.resample_interval = resample_interval
#         self.mean_periods = mean_periods
#         self.symbol = symbol
#         self.units = units
#
#         self.df_prices = pd.DataFrame(columns=[symbol])
#         self.pnl, self.upnl = 0, 0
#
#         self.bid_price, self.ask_price = 0, 0
#         self.position = 0
#         self.is_order_pending = False
#         self.is_next_signal_cycle = True
#
#     def setup_broker(self, broker):
#         broker.on_price_event = self.on_price_event
#         broker.on_order_event = self.on_order_event
#         broker.on_position_event = self.on_position_event
#         return broker
#
#     def on_price_event(self, symbol, bid, ask):
#         print(datetime.now(), '[PRICE]', symbol, 'bid:', bid, 'ask:', ask)
#
#         self.bid_price = bid
#         self.ask_price = ask
#         self.df_prices.loc[pd.Timestamp.now(), symbol] = (bid + ask) / 2.
#
#         self.get_positions()
#         self.generate_signals_and_think()
#
#         self.print_state()
#
#     def get_positions(self):
#         try:
#             self.broker.get_positions()
#         except Exception as ex:
#             print('get_positions error:', ex)
#
#     def on_order_event(self, symbol, quantity, is_buy, transaction_id, status):
#         print(
#             datetime.now(), '[ORDER]',
#             'transaction_id:', transaction_id,
#             'status:', status,
#             'symbol:', symbol,
#             'quantity:', quantity,
#             'is_buy:', is_buy,
#         )
#         if status == 'FILLED':
#             self.is_order_pending = False
#             self.is_next_signal_cycle = False
#
#             self.get_positions()  # Update positions before thinking
#             self.generate_signals_and_think()
#
#     def on_position_event(self, symbol, is_long, units, upnl, pnl):
#         if symbol == self.symbol:
#             self.position = abs(units) * (1 if is_long else -1)
#             self.pnl = pnl
#             self.upnl = upnl
#             self.print_state()
#
#     def print_state(self):
#         print(
#             datetime.now(), self.symbol, self.position_state,
#             abs(self.position), 'upnl:', self.upnl, 'pnl:', self.pnl
#         )
#
#     @property
#     def position_state(self):
#         if self.position == 0:
#             return 'FLAT'
#         if self.position > 0:
#             return 'LONG'
#         if self.position < 0:
#             return 'SHORT'
#
#     def generate_signals_and_think(self):
#         df_resampled = self.df_prices \
#             .resample(self.resample_interval) \
#             .ffill() \
#             .dropna()
#         resampled_len = len(df_resampled.index)
#
#         if resampled_len < self.mean_periods:
#             print(
#                 'Insufficient data size to calculate logic. Need',
#                 self.mean_periods - resampled_len, 'more.'
#             )
#             return
#
#         mean = df_resampled.tail(self.mean_periods).mean()[self.symbol]
#
#         # Signal flag calculation
#         is_signal_buy = mean > self.ask_price
#         is_signal_sell = mean < self.bid_price
#
#         print(
#             'is_signal_buy:', is_signal_buy,
#             'is_signal_sell:', is_signal_sell,
#             'average_price: %.5f' % mean,
#             'bid:', self.bid_price,
#             'ask:', self.ask_price
#         )
#
#         self.think(is_signal_buy, is_signal_sell)
#
#     def think(self, is_signal_buy, is_signal_sell):
#         if self.is_order_pending:
#             return
#
#         if self.position == 0:
#             self.think_when_position_flat(is_signal_buy, is_signal_sell)
#         elif self.position > 0:
#             self.think_when_position_long(is_signal_sell)
#         elif self.position < 0:
#             self.think_when_position_short(is_signal_buy)
#
#     def think_when_position_flat(self, is_signal_buy, is_signal_sell):
#         if is_signal_buy and self.is_next_signal_cycle:
#             print('Opening position, BUY',
#                   self.symbol, self.units, 'units')
#             self.is_order_pending = True
#             self.send_market_order(self.symbol, self.units, True)
#             return
#
#         if is_signal_sell and self.is_next_signal_cycle:
#             print('Opening position, SELL',
#                   self.symbol, self.units, 'units')
#             self.is_order_pending = True
#             self.send_market_order(self.symbol, self.units, False)
#             return
#
#         if not is_signal_buy and not is_signal_sell:
#             self.is_next_signal_cycle = True
#
#     def think_when_position_long(self, is_signal_sell):
#         if is_signal_sell:
#             print('Closing position, SELL',
#                   self.symbol, self.units, 'units')
#             self.is_order_pending = True
#             self.send_market_order(self.symbol, self.units, False)
#
#     def think_when_position_short(self, is_signal_buy):
#         if is_signal_buy:
#             print('Closing position, BUY',
#                   self.symbol, self.units, 'units')
#             self.is_order_pending = True
#             self.send_market_order(self.symbol, self.units, True)
#
#     def send_market_order(self, symbol, quantity, is_buy):
#         self.broker.send_market_order(symbol, quantity, is_buy)
#
#     def run(self):
#         self.broker.stream_prices(symbols=[self.symbol])
#
#
# trader = MeanReversionTrader(
#     broker,
#     resample_interval='60s',
#     symbol='EUR_USD',
#     units=1
# )
# trader.run()
#
#
#
# class TrendFollowingTrader(MeanReversionTrader):
#     def __init__(
#             self, *args, long_mean_periods=10,
#             buy_threshold=1.0, sell_threshold=1.0, **kwargs
#     ):
#         super(TrendFollowingTrader, self).__init__(*args, **kwargs)
#
#         self.long_mean_periods = long_mean_periods
#         self.buy_threshold = buy_threshold
#         self.sell_threshold = sell_threshold
#
#     def generate_signals_and_think(self):
#         df_resampled = self.df_prices \
#             .resample(self.resample_interval) \
#             .ffill().dropna()
#         resampled_len = len(df_resampled.index)
#
#         if resampled_len < self.long_mean_periods:
#             print(
#                 'Insufficient data size to calculate logic. Need',
#                 self.mean_periods - resampled_len, 'more.'
#             )
#             return
#
#         mean_short = df_resampled \
#             .tail(self.mean_periods).mean()[self.symbol]
#         mean_long = df_resampled \
#             .tail(self.long_mean_periods).mean()[self.symbol]
#         beta = mean_short / mean_long
#
#         # Signal flag calculation
#         is_signal_buy = beta > self.buy_threshold
#         is_signal_sell = beta < self.sell_threshold
#
#         print(
#             'is_signal_buy:', is_signal_buy,
#             'is_signal_sell:', is_signal_sell,
#             'beta:', beta,
#             'bid:', self.bid_price,
#             'ask:', self.ask_price
#         )
#
#         self.think(is_signal_buy, is_signal_sell)
#
# trader = TrendFollowingTrader(
#     broker,
#     resample_interval='60s',
#     symbol='EUR_USD',
#     units=1,
#     mean_periods=5,
#     long_mean_periods=10,
#     buy_threshold=1.000010,
#     sell_threshold=0.99990,
# )
# trader.run()
#
# for risk management
#     """
#     Download the all-time AAPL dataset
#     """
# from alpha_vantage.timeseries import TimeSeries
#
# # Update your Alpha Vantage API key here...
# ALPHA_VANTAGE_API_KEY = 'PZ2ISG9CYY379KLI'
#
# ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
# df, meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')
# df.info()
#
#
# # Define the date range
# start = datetime(2017, 1, 1)
# end = datetime(2017, 12, 31)
#
# # Cast indexes as DateTimeIndex objects
# df.index = pd.to_datetime(df.index)
# closing_prices = df['5. adjusted close']
# prices = closing_prices.loc[start:end]
#
#
# def calculate_daily_var(
#         portfolio, prob, mean,
#         stdev, days_per_year=252.
# ):
#     alpha = 1 - prob
#     u = mean / days_per_year
#     sigma = stdev / np.sqrt(days_per_year)
#     norminv = norm.ppf(alpha, u, sigma)
#     return portfolio - portfolio * (norminv + 1)
#
# portfolio = 100000000.00
# confidence = 0.95
#
# daily_returns = prices.pct_change().dropna()
# mu = np.mean(daily_returns)
# sigma = np.std(daily_returns)
# VaR = calculate_daily_var(
#     portfolio, confidence, mu, sigma, days_per_year=252.)
#
# print('Value-at-Risk: %.2f' % VaR)
