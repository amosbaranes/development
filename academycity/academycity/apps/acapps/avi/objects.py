import warnings
import os
from django.conf import settings
from ..ml.basic_ml_objects import BaseDataProcessing
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
from openpyxl import Workbook, load_workbook
import pandas as pd
#
from .models import TimeDim, CountryDim, MeasureDim, WorldBankFact
#
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

mpl.use('Agg')


class AviAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        print("90001-01 AviAlgo", dic, '\n', '-'*50)
        super(AviAlgo, self).__init__()
        print("90002-01 AviAlgo", dic, '\n', '-'*50)


class AviDataProcessing(BaseDataProcessing, AviAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def load_wbfile_to_db(self, dic):
        # print("90121-5: \n", dic, "="*50)
        # print(dic)
        # print('dic')
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        for k in df.columns:
            s = k.split(" ")
            # print("9088: ", s)
            try:
                y = int(s[0])
                yy, is_created = model_time_dim.objects.get_or_create(id=y)
                if is_created:
                    # yy.year = y
                    s = 'yy.' + dic["dimensions"]["time_dim"]["field_name"]+' = y'
                    # print(s)
                    exec(s)
                    yy.save()
            except Exception as ex:
                pass
        dfc = df[["Country Name", "Country Code"]]
        # print(dfc)
        for index, row in dfc.iterrows():
            # print(row["Country Name"], row["Country Name"])
            c, is_created = model_country_dim.objects.get_or_create(country_code=row["Country Code"])
            if is_created:
                # c.country_name = row["Country Name"]
                s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = "'+row["Country Name"]+'"'
                # print(s)
                exec(s)
                c.save()

        dfc = df[["Series Name", "Series Code"]]
        # print(dfc)
        for index, row in dfc.iterrows():
            # print(row["Series Name"], row["Series Code"])
            c, is_created = model_measure_dim.objects.get_or_create(measure_code=row["Series Code"])
            if is_created:
                # c.measure_name = row["Series Name"]
                s = 'c.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = "'+row["Series Name"]+'"'
                # print(s)
                exec(s)
                c.save()
        # print(df)
        for index, row in df.iterrows():
            # print('row')
            # print(row)
            for k in df.columns:
                s = k.split(" ")
                try:
                    if str(row[k]) != "nan":
                        if float("{:.2f}".format((row[k]))) > 0 or float("{:.2f}".format((row[k]))) < 0:
                            # print(row[k], float(row[k]))
                            # print("str:  ="+str(row[k])+"=")
                            y = int(s[0])
                            t = model_time_dim.objects.get(id=y)
                            c = model_country_dim.objects.get(country_code=row["Country Code"])
                            m = model_measure_dim.objects.get(measure_code=row["Series Code"])
                            a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
                            if is_created:
                                # a.amount = float(row[k])
                                s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(float("{:.2f}".format((row[k]))))
                                # print(s)
                                exec(s)
                                a.save()
                except Exception as ex:
                    pass
                    # print("90543-1" + str(ex))
        result = {"status": "ok"}
        return result

    def load_oecdfile_to_db(self, dic):
        # print("90123-5: \n", dic, "="*50)
        file_path = self.upload_file(dic)["file_path"]
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        for index, row in df.iterrows():
            try:
                if str(row["Value"]) != "nan":
                    if float("{:.2f}".format((row["Value"]))) > 0 or float("{:.2f}".format((row["Value"]))) < 0:
                        try:
                            yy = int(row["Year"])
                            t, is_created = model_time_dim.objects.get_or_create(id=yy)
                            if is_created:
                                # t.year = yy
                                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                                # print(s)
                                exec(s)
                                t.save()
                        except Exception as ex:
                            pass
                        # print("9075-11")
                        try:
                            cc = row["Country"]
                            c, is_created = model_country_dim.objects.get_or_create(country_code=cc)
                            if is_created:
                                # c.country_name = cc
                                s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = cc'
                                # print(s)
                                exec(s)
                                c.save()
                        except Exception as ex:
                            pass
                        # print("9075-22")
                        try:
                            mm = row["Measurement"]
                            # print(cc, yy, mm)
                            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm)
                            if is_created:
                                # m.measure_code = mm
                                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                                # print(s)
                                exec(s)
                                m.save()
                        except Exception as ex:
                            pass
                        # print("9075-33")
                        # print(t, c, m)
                        a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
                        if is_created:
                            # a.amount = float("{:.2f}".format((row["Value"])))
                            s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(float("{:.2f}".format((row["Value"]))))
                            # print(s)
                            exec(s)
                            a.save()
            except Exception as ex:
                print("90652-3" + str(ex))

        result = {"status": "ok"}
        return result








# class BaseDataProcessing(object):
#     def __init__(self, dic):  # to_data_path, target_field
#         self.name = 'DataProcessing'
#         # print('-'*50)
#         # print('9001 in constructor parent')
#         # print('-'*50)
#         warnings.filterwarnings(action="ignore", message="^internal gelsd")
#         # to make this notebook's output stable across runs
#
#         self.RANDOM_STATE = 42
#         np.random.seed(self.RANDOM_STATE)
#
#         # To plot pretty figures
#         mpl.rc('axes', labelsize=14)
#         mpl.rc('xtick', labelsize=12)
#         mpl.rc('ytick', labelsize=12)
#         # Where to save the figures
#         # --- Change to this when you start to use Django ---
#         self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", dic["app"])
#         # print(self.PROJECT_ROOT_DIR)
#         # print('-'*50)
#         os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)
#         self.TOPIC_ID = dic["topic_id"]  # "fundamentals"
#         self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
#         os.makedirs(self.TO_DATA_PATH, exist_ok=True)
#         self.TO_EXCEL = os.path.join(self.TO_DATA_PATH, "excel", self.TOPIC_ID)
#         os.makedirs(self.TO_EXCEL, exist_ok=True)
#         self.IMAGES_PATH = os.path.join(self.PROJECT_ROOT_DIR, "images", self.TOPIC_ID)
#         os.makedirs(self.IMAGES_PATH, exist_ok=True)
#         self.MODELS_PATH = os.path.join(self.PROJECT_ROOT_DIR, "models", self.TOPIC_ID)
#         os.makedirs(self.MODELS_PATH, exist_ok=True)
#
#         # self.TARGET_FIELD = target_field
#         # self.DATA = None
#         # self.TRAIN = None
#         # self.TEST = None
#         # self.TRAIN_TARGET = None
#         # self.TRAIN_DATA = None
#         # self.TEST_TARGET = None
#         # self.TEST_DATA = None
#         # self.train_data = None
#         # self.test_data = None
#         # self.num_attribs = None
#         # self.extra_attribs = None
#         # self.model = None
#         # self.HASH = hashlib.md5
#         # self.PIPELINE = None
#
#         # print('-'*50)
#         # print('9010 - End constructor parent')
#         # print('-'*50)
#
#     def upload_file(self, dic):
#         # print("upload_file:")
#         # print(dic)
#         # print("upload_file:")
#
#         upload_file_ = dic["request"].FILES['drive_file']
#         result = {}
#         # We can extend and add another property: data_folder
#         # like topic_id. But, we need to add this property to: params in the core view
#         # and use it here.
#         # for example: if data_folder=excel we choose self.TO_EXCEL
#
#         # print("target_folder = self.TO_"+dic["folder_type"].upper())
#         target_folder = eval("self.TO_" + dic["folder_type"].upper())
#
#         filename = dic["request"].POST['filename']
#         file_path = os.path.join(target_folder, filename)
#         with open(file_path, 'wb+') as destination:
#             for c in upload_file_.chunks():
#                 destination.write(c)
#
#         # print("9017\nUploaded\n", "-" * 30)
#         result['file_path'] = file_path
#         return result


# class DataProcessing(BaseDataProcessing):
#     def __init__(self, dic):
#         super().__init__(dic)
#
#     def get_general_data(self, dic):
#         # print("DataProcessing get_general_data 9012:\n")
#         # print(dic)
#         # print("9013:\n")
#         result = {}
#         time_dim = {}
#         country_dim = {}
#         for k in CountryDim.objects.all():
#             country_dim[k.id] = k.country_name
#
#         for k in TimeDim.objects.all():
#             time_dim[k.id] = k.year
#         result["time_dim"] = time_dim
#         result["country_dim"] = country_dim
#         return result
#
#     def load_wbfile_to_db(self, dic):
#         file_path = self.upload_file(dic)["file_path"]
#         df = pd.read_excel(file_path, sheet_name="Data", header=0)
#         # print(df)
#         n = 0
#         for k in df.columns:
#             s = k.split(" ")
#             # print("9088: ", s)
#             try:
#                 y = int(s[0])
#                 yy, is_created = TimeDim.objects.get_or_create(id=y)
#                 if is_created:
#                     yy.year = y
#                     yy.save()
#             except Exception as ex:
#                 pass
#
#         dfc = df[["Country Name", "Country Code"]]
#         # print(dfc)
#         for index, row in dfc.iterrows():
#             # print(row["Country Name"], row["Country Name"])
#             c, is_created = CountryDim.objects.get_or_create(country_code=row["Country Code"])
#             if is_created:
#                 c.country_name = row["Country Name"]
#                 c.save()
#
#         dfc = df[["Series Name", "Series Code"]]
#         # print(dfc)
#         for index, row in dfc.iterrows():
#             # print(row["Series Name"], row["Series Code"])
#             c, is_created = MeasureDim.objects.get_or_create(measure_code=row["Series Code"])
#             if is_created:
#                 c.measure_name = row["Series Name"]
#                 c.save()
#
#         # print(df)
#         for index, row in df.iterrows():
#             # print('row')
#             # print(row)
#             for k in df.columns:
#                 s = k.split(" ")
#                 try:
#                     if str(row[k]) != "nan":
#                         if float(row[k]) > 0 or float(row[k]) < 0:
#                             # print(row[k], float(row[k]))
#                             # print("str:  ="+str(row[k])+"=")
#                             y = int(s[0])
#                             t = TimeDim.objects.get(id=y)
#                             c = CountryDim.objects.get(country_code=row["Country Code"])
#                             m = MeasureDim.objects.get(measure_code=row["Series Code"])
#                             a, is_created = WorldBankFact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
#                             if is_created:
#                                 a.amount = float(row[k])
#                                 a.save()
#
#                 except Exception as ex:
#                     pass
#                     # print("90543-1" + str(ex))
#         result = {"status": "ok"}
#         return result
#
#     def load_oecdfile_to_db(self, dic):
#         # print("90123-5: \n", dic, "="*50)
#         file_path = self.upload_file(dic)["file_path"]
#         df = pd.read_excel(file_path, sheet_name="Data", header=0)
#         # print(df)
#
#         for index, row in df.iterrows():
#             try:
#                 if str(row["Value"]) != "nan":
#                     if float(row["Value"]) > 0 or float(row["Value"]) < 0:
#                         try:
#                             yy = int(row["Year"])
#                             t, is_created = TimeDim.objects.get_or_create(id=yy)
#                             if is_created:
#                                 t.year = yy
#                                 t.save()
#                         except Exception as ex:
#                             pass
#                         try:
#                             cc = row["Country"]
#                             c, is_created = CountryDim.objects.get_or_create(country_code=cc)
#                             if is_created:
#                                 c.country_name = cc
#                                 c.save()
#                         except Exception as ex:
#                             pass
#                         try:
#                             mm = row["Measurement"]
#                             print(cc, yy, mm)
#                             m, is_created = MeasureDim.objects.get_or_create(measure_name=mm)
#                             if is_created:
#                                 m.measure_code = mm
#                                 m.save()
#                         except Exception as ex:
#                             pass
#                         a, is_created = WorldBankFact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
#                         if is_created:
#                             a.amount = float(row["Value"])
#                             a.save()
#             except Exception as ex:
#                 print("90652-3" + str(ex))
#
#         result = {"status": "ok"}
#         return result

