import math
import warnings
import os
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from openpyxl import Workbook, load_workbook

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

"""
 to_data_path_ is the place datasets are kept
 topic_id name of the chapter to store images
"""
import pandas as pd
import numpy as np
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from django.apps import apps


class OptionAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 OptionAlgo", dic, '\n', '-'*50)
        try:
            super(OptionAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 OptionDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020 OptionAlgo", dic, '\n', '-'*50)


class OptionDataProcessing(BaseDataProcessing, BasePotentialAlgo, OptionAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def data_upload(self, dic):
        print("90121-1: \n", "="*50, "\n", dic, "\n", "="*50)

        try:
            app_ = dic["app"]
            file_path = self.upload_file(dic)["file_path"]
            ticker_=file_path.split("/")[-1].split(".")[0]
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
        print(df)
        print(df.columns)

        # for f_ in df.columns:
        #     try:
        #         print(f_)
        #         var_obj, is_created = model_var_dim.objects.get_or_create(var_code=f_)
        #         var_obj.var_group_dim=group_obj
        #         var_obj.var_code = f_
        #         var_obj.save()
        #         print(group_obj, f_)
        #         print(var_obj)
        #     except Exception as ex:
        #         print("Error 90121-300", ex)
        #
        #     for index, row in df.iterrows():
        #         # print(row)
        #         n_ = 0
        #         entity_code_ = str(row[1]).strip()
        #         # print("=" * 50)
        #         try:
        #             # print(entity_code_)
        #             entity_obj, is_created = model_entity_dim.objects.get_or_create(entity_code=entity_code_)
        #             if is_created:
        #                 entity_obj.entity_code = entity_code_
        #                 entity_obj.save()
        #         except Exception as ex:
        #             print("Error 90121-400", ex)
        #         try:
        #             v_ = float(str(row[f_]))
        #             if v_ is not None and str(v_) != "nan":
        #                 # print(row[columns[j]], float(str(row[columns[j]])))
        #                 fact_obj, is_created = model_fact.objects.get_or_create(entity_dim=entity_obj,
        #                                                                         var_dim=var_obj)
        #                 fact_obj.amount = v_
        #                 fact_obj.save()
        #         except Exception as ex:
        #             print("Error 90121-500", ex)

        wb.close()

        result = {"status": "ok"}
        print(result)

        return result


class Option(object):
    def __init__(self):
        pass

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


    def test1(self, dic):
        print('90-90-90-11 data_transfer_to_process_fact 90055-300 dic\n', '-'*100, '\n', dic, '\n', '-'*100)
        app_ = dic["app"]
        # S = float(dic["S"])
        K = float(dic["K"])
        sigma = float(dic["sigma"])
        T = int(dic["T"])
        r = float(dic["r"])
        n = int(dic["n"])
        t = int(dic["t"])
        T = T-t/n

        x=[]
        lp=[]
        lc=[]
        for i in range(1, 200, 1):
            c = self.call(i, K, T, r, sigma, n)
            p = self.put(i, K, T, r, sigma, n)
            x.append(i)
            lc.append(c)
            lp.append(p)

        # print(lc, lp)

        result = {"status": "ok", "data": {"x":x, "lc":lc, "lp":lp}}
        return result
