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

# ======================================
# This project can work for covid, neck
#
# ======================================

class CovidAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 CovidAlgo", dic, '\n', '-'*50)
        try:
            super(CovidAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 CovidDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020 CovidAlgo", dic, '\n', '-'*50)


class CovidDataProcessing(BaseDataProcessing, BasePotentialAlgo, CovidAlgo):
    def __init__(self, dic):
        super().__init__(dic)
        app_ = dic["app"]
        self.Debug = apps.get_model(app_label=app_, model_name="debug")

    def log_debug(self, value):
        self.Debug.objects.create(value=value)

    def clear_log_debug(self):
        self.Debug.truncate()

    def data_upload(self, dic):
        print("90121-1: \n", "="*50, "\n", dic, "\n", "="*50)
        try:
            app_ = dic["app"]
            file_path = self.upload_file(dic)["file_path"]
            # print(file_path)
            sheet_name = dic["sheet_name"]
            s = sheet_name.split("_")
            sheet_name = s[0]
            dic = dic["cube_dic"]
            # print('90121-3 dic', dic)

            model_name_ = dic["dimensions"]["entity_dim"]["model"]
            model_entity_dim = apps.get_model(app_label=app_, model_name=model_name_)
            #
            model_name_ = dic["dimensions"]["var_group_dim"]["model"]
            model_var_group_dim = apps.get_model(app_label=app_, model_name=model_name_)
            #
            model_name_ = dic["dimensions"]["var_dim"]["model"]
            model_var_dim = apps.get_model(app_label=app_, model_name=model_name_)
            #
            model_name_ = dic["fact"]["model"]
            model_fact = apps.get_model(app_label=app_, model_name=model_name_)
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
        df = df.reset_index()  # make sure indexes pair with number of rows
        # print(df)

        numb_indep_vars = -1
        if numb_indep_vars < 0:
            for c in columns_:
                numb_indep_vars += 1
                if c == "end_indeps":
                    df.drop(['end_indeps'], inplace=True, axis=1)
                    break

        # print(numb_indep_vars)
        columns_ = df.columns[1:]

        print(columns_)

        for i in range(len(columns_)):
            f_ = columns_[i]
            if i > 0:
                if i < numb_indep_vars:
                    # print("="*10, "\nindep ", f_, "\n", "-"*10)
                    group_obj, is_created = model_var_group_dim.objects.get_or_create(group_name='indep')
                else:
                    # print("="*10, "\ndep ", f_, "\n", "-"*10)
                    group_obj, is_created = model_var_group_dim.objects.get_or_create(group_name='dep')
                try:
                    # print(f_)
                    var_obj, is_created = model_var_dim.objects.get_or_create(var_code=f_)
                    var_obj.var_group_dim=group_obj
                    var_obj.var_code = f_
                    var_obj.save()
                    # print(group_obj, f_)
                    # print(var_obj)
                except Exception as ex:
                    print("Error 90121-300", ex)

                for index, row in df.iterrows():
                    # print(row)
                    n_ = 0
                    entity_code_ = str(row[1]).strip()
                    # print("=" * 50)
                    try:
                        # print(entity_code_)
                        entity_obj, is_created = model_entity_dim.objects.get_or_create(entity_code=entity_code_)
                        if is_created:
                            entity_obj.entity_code = entity_code_
                            entity_obj.save()
                    except Exception as ex:
                        print("Error 90121-400", ex)
                    try:
                        v_ = float(str(row[f_]))
                        if v_ is not None and str(v_) != "nan":
                            # print(row[columns[j]], float(str(row[columns[j]])))
                            fact_obj, is_created = model_fact.objects.get_or_create(entity_dim=entity_obj,
                                                                                    var_dim=var_obj)
                            fact_obj.amount = v_
                            fact_obj.save()
                    except Exception as ex:
                        print("Error 90121-500", ex)
        wb.close()

        result = {"status": "ok"}
        # print(result)

        return result

