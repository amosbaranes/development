from ...ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
import math
import warnings
import os

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

from django.apps import apps
# ---
import yfinance as yf
import quandl
from scipy import stats
from alpha_vantage.timeseries import TimeSeries
from abc import ABC, abstractmethod
import v20

from pathlib import Path
from copy import deepcopy
# ----
import warnings
warnings.filterwarnings('ignore')


# =========== Working but Not used =====================
class DeepLearning(object):
    # print("CC1 DeepLearning")
    def __init__(self, dic):
        # print("CC5 DeepLearning\n", "-"*100, "\n", dic, "\n", "-"*100)
        np.random.seed(seed=42)


class MLAT(BaseDataProcessing, BasePotentialAlgo, DeepLearning):
    def __init__(self, dic):
        # print("AA2 MLAT\n", "-"*100, "\n", dic, "\n", "-"*100)
        # super().__init__(dic)
        super(MLAT, self).__init__(dic)

        self.RESULT_PATH = os.path.join(self.PROJECT_ROOT_DIR, "mlat_results")
        os.makedirs(self.RESULT_PATH, exist_ok=True)

    # Gets data for internal and external circles.
    def test(self, dic):
        print(" 90-100-1 MLAT.test\n", "-"*100, "\n", dic, "\n", "-"*100)

        N = 50000
        factor = 0.1
        noise = 0.1

        n_iterations = 50000
        learning_rate = 0.0001
        momentum_factor = .5

        # generate data
        X, y = make_circles(n_samples=N,shuffle=True,factor=factor,noise=noise)
        # define outcome matrix
        # print("y\n", y)

        Y = np.zeros((N, 2))
        for c in [0, 1]:
            Y[y == c, c] = 1
        print("Y\n", Y)
        print("X\n", X)

        result = {"status": "ok"}
        # print(result)
        return result

# ==========================================
class StockOption(object):
    def __init__(self, S0, K, r=0.05, T=1, N=2, pu=0, pd=0,div=0, sigma=0, is_put=False, is_am=False):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N)
        self.STs = [] # Declare the stock prices tree
        self.pu, self.pd = pu, pd
        self.div = div
        self.sigma = sigma
        self.is_call = not is_put
        self.is_european = not is_am

    @property
    def dt(self):
        return self.T/float(self.N)

    @property
    def df(self):
        return math.exp(-(self.r-self.div)*self.dt)


class BinomialEuropeanOption(StockOption):
    def setup_parameters(self):
        self.M = self.N+1 # Number of terminal nodes of tree
        self.u = 1+self.pu # Expected value in the up state
        self.d = 1-self.pd # Expected value in the down state
        self.qu = (math.exp((self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def init_stock_price_tree(self):
        self.STs = np.zeros(self.M)
        for i in range(self.M):
            self.STs[i] = self.S0 * (self.u**(self.N-i)) * (self.d**i)

    def init_payoffs_tree(self):
        if self.is_call:
            return np.maximum(0, self.STs-self.K)
        else:
            return np.maximum(0, self.K-self.STs)

    def traverse_tree(self, payoffs):
        for i in range(self.N):
            payoffs = (payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
        return payoffs

    def begin_tree_traversal(self):
        payoffs = self.init_payoffs_tree()
        return self.traverse_tree(payoffs)

    def price(self):
        self.setup_parameters()
        self.init_stock_price_tree()
        payoffs = self.begin_tree_traversal()
        return payoffs[0]


# =================================================
class OptionAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 OptionAlgo", dic, '\n', '-'*50)
        try:
            super(OptionAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 OptionDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020 OptionAlgo", dic, '\n', '-'*50)

    def call(self, S, K, T, r, sigma, n):
        dt = T / n
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)
        option_price_c = [max(0, S * (u ** (n - i)) * (d ** i) - K) for i in range(n + 1)]

        for j in range(n - 1, -1, -1):
            for i in range(j + 1):
                option_price_c[i] = max(S * (u ** (j - i)) * (d ** i) - K,
                                        math.exp(-r * dt) * (
                                                    p * option_price_c[i] + (1 - p) * option_price_c[i + 1]))

        return round(100 * option_price_c[0]) / 100

    def put(self, S, K, T, r, sigma, n):
        dt = T / n
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)

        option_price_p = [max(0, K - S * (u ** (n - i)) * (d ** i)) for i in range(n + 1)]

        for j in range(n - 1, -1, -1):
            for i in range(j + 1):
                option_price_p[i] = max(K - S * (u ** (j - i)) * (d ** i),
                                        math.exp(-r * dt) * (
                                                    p * option_price_p[i] + (1 - p) * option_price_p[i + 1]))

        return round(100 * option_price_p[0]) / 100

    def calc_options(self, dic):
        print('90055-300 calc_options\n', '-'*100, '\n', dic, '\n', '-'*100)
        app_ = dic["app"]
        # S = float(dic["S"])
        spread = 5
        try:
            spread = float(dic["spread"])
        except Exception as ex:
            pass
        K = float(dic["K"])
        sigma = float(dic["sigma"])
        T = int(dic["T"])
        r = float(dic["r"])
        r = 0.007
        n = int(dic["n"])
        t = int(dic["t"])
        T = T*(1-t/n)

        x=[]
        lp=[]
        lc=[]
        lps=[]
        lcs=[]

        # d = 1
        # nn = int(0.25 * K)
        #
        # print(K, int(K) - nn, int(K) + nn)
        #
        # for i in range(int(K) - nn, int(K) + nn, 1):

        nn = 100
        f = 0.4
        if K < 10:
            f = 1
        elif K < 20:
            f = 0.8
        elif K < 30:
            f = 0.6
        elif K < 100:
            f = 0.5
        elif K < 200:
            f = 0.45
        elif K < 300:
            f = 0.45
        elif K < 400:
            f = 0.4
        elif K < 500:
            f = 0.3
        elif K < 1000:
            f = 0.4
        elif K < 2000:
            f = 0.5
        elif K < 6000:
            f = 0.04

        step = f*K/nn

        for i in range(0, nn, 1):
            si = K + (i - n/2)*step

            c = self.call(si, K, T, r, sigma, n)
            cs = self.call(si, K-spread, T, r, sigma, n)

            #
            p = self.put(si, K, T, r, sigma, n)
            ps = self.put(si, K+spread, T, r, sigma, n)
            #
            x.append(si)
            lc.append(c)
            lp.append(p)
            lcs.append(cs)
            lps.append(ps)

        # print(lc, lp)

        result = {"status": "ok", "data": {"x":x, "lc":lc, "lp":lp, "lcs":lcs, "lps":lps}}
        return result


class OptionDataProcessing(BaseDataProcessing, BasePotentialAlgo, OptionAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    # download daily data from yahoo finance
    # and call process_std
    def get_stock_prices_days(self, dic):
        print("90300-100-00: \n", "="*50, "\n", dic, "\n", "="*50)
        ticker_ = dic["ticker"]
        app_ = dic["app"]
        model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
        company_obj, is_created = model_company_info.objects.get_or_create(ticker=ticker_)
        company_obj.company_name=ticker_
        company_obj.save()
        #
        model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")
        #

        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5000)
            df = yf.download(ticker_, start_date, end_date)
            # print("A\n", df)
            df = df.drop('Close', 1).rename(columns={"Adj Close": "Close"})
            # print("B\n", df)
            df = df.reset_index()
            # print(df)
            for index, row in df.iterrows():
                d = str(row["Date"]).split(" ")
                dd = d[0].split("-")
                idx_ = int(dd[0])*10000+int(dd[1])*100+int(dd[2])
                # print(idx_)
                open_ = float(row["Open"])
                high_ = float(row["High"])
                low_ = float(row["Low"])
                close_ = float(row["Close"])
                volume_ = int(int(row["Volume"])/1000)
                # print(idx_, open_,high_,low_,close_,volume_)
                try:
                    price_obj, is_created = model_stockpricesdays.objects.get_or_create(company=company_obj, idx=idx_)
                    price_obj.open = open_
                    price_obj.high = high_
                    price_obj.low = low_
                    price_obj.close = close_
                    price_obj.volume = volume_
                    price_obj.save()
                except Exception as ex:
                    print("Error 90121-400", ex)
        except Exception as ex:
            print("Error 111:", ex)

        try:
            self.process_std(dic)
        except Exception as ex:
            print("Error 55-55-11-1", ex)
        result = {"status": "ok"}
        print("get_stock_prices_days: ", result)
        return result

    # upload excel # to be deleted
    def data_upload(self, dic):
        print("90121-200: \n", "="*50, "\n", dic, "\n", "="*50)

        try:
            app_ = dic["app"]
            file_path = self.upload_file(dic)["file_path"]
            # print(file_path)

            ticker_=file_path.split("/")[-1].split(".")[0]
            # print(ticker_)

            sheet_name = dic["sheet_name"]
            dic = dic["cube_dic"]
            # print('90121-3 dic', dic)

            model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
            company_obj, is_created = model_company_info.objects.get_or_create(ticker=ticker_)
            company_obj.company_name=ticker_
            company_obj.save()
            #
            model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")
            #
        except Exception as ex:
            print("Error 90121-100", ex)

        wb = load_workbook(filename=file_path, read_only=False)
        ws = wb[sheet_name]
        data = ws.values

        columns_ = next(data)[0:]   # Get the first line in file as a header line
        # print(columns_)
        # Create a DataFrame based on the second and subsequent lines of data
        df = pd.DataFrame(data, columns=columns_)
        # print(df)
        # print(df.columns)

        for index, row in df.iterrows():
            # print(row)
            n_ = 0
            idx_ = str(row[0]).split("/")
            idx_ = int(idx_[2])*10000+int(idx_[0])*100+int(idx_[1])

            close_ = float(str(row[1]).replace('$', ''))
            volume_ = int(str(row[2]))
            open_ = float(str(row[3]).replace('$', ''))
            high_ = float(str(row[4]).replace('$', ''))
            low_ = float(str(row[5]).replace('$', ''))

            # print("=" * 50)
            try:
                price_obj, is_created = model_stockpricesdays.objects.get_or_create(company=company_obj, idx=idx_)
                price_obj.close = close_
                price_obj.volume = volume_
                price_obj.open = open_
                price_obj.high = high_
                price_obj.low = low_
                price_obj.save()
            except Exception as ex:
                print("Error 90121-400", ex)

        wb.close()

        result = {"status": "ok"}
        print(result)

        return result

    # calculate yearly and monthly(for every month of every year) std
    # and save the results in database
    def process_std(self, dic):
        print("90300-300: \n", "="*50, "\n", dic, "\n", "="*50)
        try:
            app_ = dic["app"]
            model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")
            model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
            ticker_ = dic["ticker"]
            company_obj = model_company_info.objects.get(ticker=ticker_)
            year_ = "all"
            try:
                year_ = int(dic["year"])
            except Exception as ex:
                pass
            num_of_bars = 999999999
            # num_of_bars = int(dic["num_of_bars"])
            # print("ticker", ticker)
            if year_ == "all":
                sp = model_stockpricesdays.objects.filter(company__ticker=ticker_)[:num_of_bars]
            else:
                year_h = (year_+1)*10000
                year_l = year_*10000
                # print(year_l, year_h)
                print(ticker_)
                sp = model_stockpricesdays.objects.filter(company__ticker=ticker_, idx__gte=year_l, idx__lte=year_h)[:num_of_bars]

            # df = pd.DataFrame(list(sp.values()))
            df = pd.DataFrame(list(sp.values("idx", "open", "close", "high", "low", "volume")))
            df['idx'] = pd.to_datetime(df['idx'], format='%Y%m%d')
            df.set_index('idx', inplace=True)
            df.sort_index(inplace=True)
            # print("AA\n", df)
            df['A'] = df.index
            dfs = df.shift(periods=1)
            # print("dfs\n", dfs)
            df = pd.merge(left=df, right=dfs, left_index=True, right_index=True)
            # print(df)
            df.dropna(inplace=True)
            df["return"] = (df["close_x"]-df["close_y"])/df["close_y"]
            # print("df\n", df)

            try:
                df["A_y"] = df["A_x"]
                # print("df1111\n", df)
                rr = df.groupby([df["A_x"].dt.year, df["A_y"].dt.month])["return"].std()
                # print(rr)
                rr = rr.reset_index()
                rr.dropna(inplace=True)
                rr["idx"] = rr["A_x"]*100+rr["A_y"]
                rr = rr.drop('A_x', 1).drop('A_y', 1)
                rr = rr.rename(columns={"return": "std"})
                # print(rr)
                model_stockreturnstd = apps.get_model(app_label=app_, model_name="stockreturnstd") #
                for index, row in rr.iterrows():
                    price_obj, is_created = model_stockreturnstd.objects.get_or_create(company=company_obj,
                                                                                       idx=int(row["idx"]))
                    price_obj.amount = float(row["std"])
                    price_obj.save()
            except Exception as ex:
                print("Error 2020-20-1", ex)

            try:
                # print("df1111\n", df)
                rr = df.groupby([df["A_x"].dt.year])["return"].std()
                rr = rr.reset_index()
                rr.dropna(inplace=True)

                rr["idx"] = rr["A_x"]*100
                # print(rr)
                rr = rr.drop('A_x', 1)
                rr = rr.rename(columns={"return": "std"})
                # print(rr)

                model_stockreturnstd = apps.get_model(app_label=app_, model_name="stockreturnstd") #
                for index, row in rr.iterrows():
                    price_obj, is_created = model_stockreturnstd.objects.get_or_create(company=company_obj,
                                                                                       idx=int(row["idx"]))
                    price_obj.amount = float(row["std"])
                    price_obj.save()
            except Exception as ex:
                print("Error 2020-20-1", ex)

        except Exception as ex:
            print("Error 90300-100-5", ex)
        result = {"status": "ok"}
        print("process_std: ", result)
        return result

    # the function process_std calculate yearly and monthly std.
    # So, this function can e deleted.
    def process_yearly_std(self, dic):
        print("90300-400: \n", "="*50, "\n", dic, "\n", "="*50)

        try:
            app_ = dic["app"]
            model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")
            model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
            ticker_ = dic["ticker"]
            company_obj = model_company_info.objects.get(ticker=ticker_)
            year_ = "all"
            try:
                year_ = int(dic["year"])
            except Exception as ex:
                pass

            num_of_bars = 999999999

            # num_of_bars = int(dic["num_of_bars"])
            # print("ticker", ticker)

            if year_ == "all":
                sp = model_stockpricesdays.objects.filter(company__ticker=ticker_)[:num_of_bars]
            else:
                year_h = (year_+1)*10000
                year_l = year_*10000
                # print(year_l, year_h)
                print(ticker)
                sp = model_stockpricesdays.objects.filter(company__ticker=ticker_, idx__gte=year_l, idx__lte=year_h)[:num_of_bars]

            # df = pd.DataFrame(list(sp.values()))
            df = pd.DataFrame(list(sp.values("idx", "open", "close", "high", "low", "volume")))
            df['idx'] = pd.to_datetime(df['idx'], format='%Y%m%d')
            df.set_index('idx', inplace=True)
            df.sort_index(inplace=True)
            # print("AA\n", df)
            df['A'] = df.index
            dfs = df.shift(periods=1)
            # print("dfs\n", dfs)
            df = pd.merge(left=df, right=dfs, left_index=True, right_index=True)
            # print(df)
            df.dropna(inplace=True)
            df["return"] = (df["close_x"]-df["close_y"])/df["close_y"]
            # print("df\n", df)

            try:
                # print("df1111\n", df)
                rr = df.groupby([df["A_x"].dt.year])["return"].std()
                rr = rr.reset_index()
                rr.dropna(inplace=True)

                rr["idx"] = rr["A_x"]*100
                # print(rr)
                rr = rr.drop('A_x', 1)
                rr = rr.rename(columns={"return": "std"})
                print(rr)

                model_stockreturnstd = apps.get_model(app_label=app_, model_name="stockreturnstd") #
                for index, row in rr.iterrows():
                    price_obj, is_created = model_stockreturnstd.objects.get_or_create(company=company_obj,
                                                                                       idx=int(row["idx"]))
                    price_obj.amount = float(row["std"])
                    price_obj.save()
            except Exception as ex:
                print("Error 2020-20-1", ex)


            sigma_ = 10
        except Exception as ex:
            print("Error 90300-100-6", ex)
        result = {"status": "ok", "sigma": sigma_}
        print(result)


        return result

    def get_return_std(self, dic):
        print("90300-500 get_return_std: \n", "="*50, "\n", dic, "\n", "="*50)
        ticker_ = dic["ticker"]
        app_ = dic["app"]
        model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
        company_obj = model_company_info.objects.get(ticker=ticker_)
        #
        model_stockreturndays = apps.get_model(app_label=app_, model_name="StockReturnStd")
        #
        model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")
        close_stock_price = round(100*float(model_stockpricesdays.objects.filter(company__ticker=ticker_).all().first().close))/100
        #
        qs = model_stockreturndays.objects.filter(company=company_obj).all()
        df = pd.DataFrame(list(qs.values("idx", "amount")))
        # print("AA\n", df)

        re = {"idx": [], "std":[], "yidx":[], "ystd":[], "close_stock_price":close_stock_price}
        for index, row in df.iterrows():
            s = str(row["idx"])
            y=s[0:4]
            m=s[4:7]
            if m == "00":
                re["yidx"].append(y)
                re["ystd"].append(float(row["amount"]))
            else:
                re["idx"].append(y+"-"+m)  # str(row["idx"])
                re["std"].append(float(row["amount"]))

        dic["K"] = close_stock_price
        dic["sigma"] = re["std"][-1]
        re_ = self.calc_options(dic)

        result = {"status": "ok", "data": re, "datao": re_["data"]}
        # print(result)
        return result

    def test(self, dic):
        print("90300-600-900: \n", "="*50, "\n", dic, "\n", "="*50)
        app_ = dic["app"]

        # -- yf --
        ticker_ = '^GSPC'
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3000)
        df_gspc = yf.download(ticker_, start_date, end_date)
        df_gspc = df_gspc.drop('Close', 1).rename(columns={"Adj Close": "Close"})
        # df_gspc = df_gspc.iloc[[1]]
        ticker_ = '^VIX'
        df_vix = yf.download(ticker_, start_date, end_date)
        df_vix = df_vix.drop('Close', 1).rename(columns={"Adj Close": "Close"})
        # df_vix = df_vix.iloc[[1]]
        # print(df_gspc, "\n\n", df_vix)
        df = pd.merge(left=df_gspc, right=df_vix, left_index=True, right_index=True)
        df = df[["Close_x", "Close_y"]]
        df.rename(columns={"Close_x": "SPX", "Close_y": "VIX"}, inplace=True)
        print("AA\n", df)
        df.index = pd.to_datetime(df.index)
        print("C \n", df, "\ndescribe\n", df.describe(), "\ninfo\n", df.info())

        # print(df)
        # print(df.shift(1))
        # print(df / df.shift(1))
        log_returns = np.log(df / df.shift(1)).dropna()
        corr = log_returns.corr()
        print(corr)

        # # -- quandl --
        # QUANDL_API_KEY = 'qjAWtEj_sxwdficXiePo'
        # quandl.ApiConfig.api_key = QUANDL_API_KEY

        # df = quandl.get(
        #     'CHRIS/CME_GC1',
        #     column_index=6,
        #     collapse='monthly',
        #     start_date='2000-01-01')
        # print(df.head)
        # df_settle = df['Settle'].resample('MS').ffill().dropna()
        # df_rolling = df_settle.rolling(12)
        # df_mean = df_rolling.mean()
        # df_std = df_rolling.std()
        # print(df_mean, df_std)

        # https://www.slickcharts.com/sp500


        # SYMBOLS = ['AAPL', 'MMM', 'AXP', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DD', 'XOM','GS', 'HD', 'IBM', 'INTC', 'JNJ',
        #     'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'UNH', 'UTX', 'TRV', 'VZ', 'V', 'WMT', 'WBA', 'DIS',]
        #
        # wiki_symbols = ['WIKI/%s' % symbol for symbol in SYMBOLS]
        #
        # start_date = '2018-01-01'
        # end_date = '2024-06-10'
        # df_components = quandl.get(
        #                         wiki_symbols,
        #                         start_date=start_date,
        #                         end_date=end_date,
        #                         column_index=11)
        # df_components.columns = SYMBOLS # Renaming the columns
        # # print("Ad\n", df_components)
        # filled_df_components = df_components.fillna(method='ffill')
        # daily_df_components = filled_df_components.resample('24h').ffill()
        # daily_df_components = daily_df_components.fillna(method='bfill')
        # print("Ad3\n", daily_df_components)
        #
        a =100
        # Not working
        # try:
        #     ALPHA_VANTAGE_API_KEY = 'J9ZMYFC1WI8GAJSR'
        #     ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        #
        #     df_spx, meta_data = ts.get_daily_adjusted(symbol='^GSPC', outputsize='full')
        #     print(df_spx)
        #
        #     # df_dji, meta_data = ts.get_daily_adjusted(symbol='^DJI', outputsize='full')
        #     # print(df)
        # except Exception as ex:
        #     print(ex)





        # df = quandl.get('EURONEXT/ABN.4')
        # print("A quandl\n", df)
        # daily_changes = df.pct_change(periods=1).dropna()
        # print(daily_changes)
        # df_std = daily_changes.rolling(window=30, min_periods=30).std()
        # print(df_std)
        #
        # df_filled = df.asfreq('D', method='ffill')
        # df_last = df['Last']
        # series_short = df_last.rolling(window=5, min_periods=5).mean()
        # series_long = df_last.rolling(window=30, min_periods=30).mean()
        # #
        # series_short_e = df_last.ewm(span=5).mean()
        # series_long_e = df_last.ewm(span=30).mean()
        # #
        # df_sma = pd.DataFrame(columns=['short', 'long', 'shorte', 'longe'])
        # df_sma['short'] = series_short
        # df_sma['long'] = series_long
        # df_sma['shorte'] = series_short_e
        # df_sma['longe'] = series_long_e
        #
        # print(df_sma)
        #
        # df_sma = df_sma.dropna()
        # print(df_sma)

        # eu_option = BinomialEuropeanOption(50, 52, r=0.05, T=2, N=2, pu=0.2, pd=0.2, is_put=False)
        # print('European put option price is:', eu_option.price())

        result = {"status": "ok"}
        # print(result)
        return result


