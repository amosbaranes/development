import warnings
import os
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
# from openpyxl import Workbook, load_workbook

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


class AviaDataProcessing(BaseDataProcessing, BasePotentialAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def check_country(self, cc):
        if cc == "Viet Nam":
            cc = "Vietnam"
        elif cc == "Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "DR Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "Democratic Republic Of The Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "Congo":
            cc = "Republic of the Congo"
        elif cc == "Republic of the Congo":
            cc = "Congo, Rep."
        elif cc == "Russian Federation":
            cc = "Russia"
        elif cc == "Côte d’Ivoire":
            cc = "Cote d'Ivoire"
        elif cc == "Ivory Coast":
            cc = "Cote d'Ivoire"
        elif cc == "Eswatini (Swaziland)":
            cc = "Eswatini"
        elif cc == "Slovak Republic":
            cc = "Slovakia"
        elif cc == "Korea":
            cc = "South Korea"
        elif cc == "Republic Of Korea":
            cc = "South Korea"
        elif cc == "Korea, Dem. People's Rep":
            cc = "North Korea"
        elif cc == "United States Of America":
            cc = "United States"
        elif cc == "Cabo Verde":
            cc = "Cape Verde"
        elif cc == "United Republic Of Tanzania":
            cc = "Tanzania"
        elif cc == "Guinea Bissau":
            cc = "Guinea-bissau"
        elif cc == "Lao People's Democratic Republic":
            cc = "Laos"
        elif cc == "Republic Of Moldova":
            cc = "Moldova"
        elif cc == "Republic Of North Macedonia":
            cc = "North Macedonia"
        elif cc == "Macedonia":
            cc = "North Macedonia"
        elif cc == "EU (27)":
            cc = "EU27"
        elif cc == "Yemen, Rep.":
            cc = "Yemen"
        elif cc == "Venezuela, RB":
            cc = "Venezuela"
        elif cc == "turkiye":
            cc = "turkey"
        elif cc == "Egypt, Arab Rep.":
            cc = "Egypt"
        elif cc == "China (Mainland)":
            cc = "China"
        elif cc == "Hong Kong SAR":
            cc = "China-Hong Kong"
        elif cc == "Hong Kong (China)":
            cc = "China-Hong Kong"
        elif cc == "Hong Kong":
            cc = "China-Hong Kong"
        elif cc == "USA":
            cc = "United States"
        elif cc == "Slovak Republic":
            cc = "Slovakia"
        elif cc == "Macau":
            cc = "China-Macau"
        elif cc == "Cabo Verde":
            cc = "Cape Verde"
        elif cc == "United Republic Of Tanzania":
            cc = "Tanzania"
        elif cc == "Guinea Bissau":
            cc = "Guinea-bissau"
        elif cc == "Republic Of Moldova":
            cc = "Moldova"
        return cc

    def check_city(self, cc):
        if cc == "Tel Aviv-Yafo":
            cc = "Tel Aviv"
        if cc == "Washington":
            cc = "Washington, DC"
        return cc

    def load_Smart_City_indexes_to_db(self, dic):
        # print("90121-555: \n", dic, "\n", "="*50)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)

        field_name_ = dic["dimensions"]["time_dim"]["field_name"]

        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        yy = 2019
        t, is_created = model_time_dim.objects.get_or_create(id=yy)
        if is_created:
            s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
            exec(s)
            t.save()

        model_name_ = dic["dimensions"]["city_dim"]["model"]
        model_city_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "countrydim"
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        # print(df.columns[3:])
        for index, row in df.iterrows():
            # print(row["city"], row["country"], row["Mobility"], row["Environment"], row["Government"], row["Economy"],
            #       row["People"], row["Living"], row["Index"], row["relative_Edmonton"])
            # Country
            try:
                cc = self.check_country(str(row["country"]))
                c, is_created = model_country_dim.objects.get_or_create(country_code=cc)
                if is_created:
                    s = 'c.country_name' + ' = "' + cc + '"'
                    exec(s)
                    c.save()
            except Exception as ex:
                print("90987-1 Error measure:"+str(ex))
            # City
            try:
                city, is_created = model_city_dim.objects.get_or_create(country_dim=c, city_name=row["city"])
            except Exception as ex:
                print("90987-2 Error measure:"+str(ex))

            for k in df.columns[3:]:
                # print(k, row[k])
                g, is_created = model_group_measure_dim.objects.get_or_create(group_name=k)
                m, is_created = model_measure_dim.objects.get_or_create(measure_group_dim=g, measure_name=k)
                f, is_created = model_fact.objects.get_or_create(time_dim=t, city_dim=city, measure_dim=m)
                f.amount=row[k]
                f.save()

        result = {"status": "ok"}
        return result

    def load_Smart_City_salary_to_db(self, dic):
        print("90121-545: \n", dic, "\n", "="*50)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)

        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        yy = 2019
        t, is_created = model_time_dim.objects.get_or_create(id=yy)
        if is_created:
            s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
            exec(s)
            t.save()

        model_name_ = dic["dimensions"]["city_dim"]["model"]
        model_city_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = "countrydim"
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        for index, row in df.iterrows():
            s_city = str(row["city"]).split(",")[0].strip()
            s_country = str(row["city"]).split(",")[-1].strip()
            # print(s_city, s_country, row["net_salary"])
            # Country
            try:
                cc = self.check_country(s_country)
                c, is_created = model_country_dim.objects.get_or_create(country_code=cc)
                if is_created:
                    s = 'c.country_name' + ' = "' + cc + '"'
                    exec(s)
                    c.save()
            except Exception as ex:
                print("90987-1 Error measure:"+str(ex))
            # City
            try:
                s_city = self.check_city(s_city)
                city, is_created = model_city_dim.objects.get_or_create(country_dim=c, city_name=s_city)
            except Exception as ex:
                print("90987-2 Error measure:"+str(ex))

            for k in df.columns[2:]:
                # print(k, row[k])
                g, is_created = model_group_measure_dim.objects.get_or_create(group_name=k)
                m, is_created = model_measure_dim.objects.get_or_create(measure_group_dim=g, measure_name=k)
                f, is_created = model_fact.objects.get_or_create(time_dim=t, city_dim=city, measure_dim=m)
                f.amount=row[k]
                f.save()
        result = {"status": "ok"}
        return result

