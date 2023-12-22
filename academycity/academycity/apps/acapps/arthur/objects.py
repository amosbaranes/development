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


class ArthurAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 AvibAlgo", dic, '\n', '-'*50)
        try:
            super(ArthurAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 AvibDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020 AvibAlgo", dic, '\n', '-'*50)


class ArthurDataProcessing(BaseDataProcessing, BasePotentialAlgo, ArthurAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def data_upload(self, dic):
        print("90121-1: \n", "="*50, "\n", dic, "\n", "="*50)
        try:
            app_ = dic["app"]
            file_path = self.upload_file(dic)["file_path"]
            print(file_path)
            sheet_name = dic["sheet_name"]
            dic = dic["cube_dic"]
            # print('90121-3 dic', dic)

            model_name_ = dic["dimensions"]["entity_dim"]["model"]
            model_entity_dim = apps.get_model(app_label=app_, model_name=model_name_)
            #
            model_name_ = dic["dimensions"]["measure_dim"]["model"]
            model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
            model_measure_group_dim = apps.get_model(app_label=app_, model_name="measuregroupdim")
            #
            model_name_ = dic["fact"]["model"]
            model_fact = apps.get_model(app_label=app_, model_name=model_name_)
            #
            model_min_max_cut = apps.get_model(app_label=app_, model_name="minmaxcut")
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
        min_cut = []
        max_cut = []

        dic_ = {"svbw5": ["svbw4", "svbw6"],
                "svbl5":["svbl3", "ivbl3", "svbl4", "ivbl4", "ivbl5", "svbl6", "ivbl6", "svbl7", "ivbl7"],
                "ivbl5": ["svbl3", "ivbl3", "svbl4", "ivbl4", "svbl5", "svbl6", "ivbl6", "svbl7", "ivbl7", "height"],
                "ivbw5":["sex-dependent", "ivbw3", "ivbw4", "svbl4", "svbw6", "ivbw6", "svbw7", "ivbl7"],
                "afvbh5":["afvbh3", "afvbh4", "afvbh6", "lsvbh6"]}
        for f in dic_:
            # Group
            try:
                print("="*20, "\n", f, "\n", "-"*20)
                columns = dic_[f]
                group_obj, is_created = model_measure_group_dim.objects.get_or_create(group_name=f)
                if is_created:
                    group_obj.group_name = f
                    group_obj.save()
            except Exception as ex:
                print("Error 90121-200", ex)
            #
            for f_ in columns:
                print("1"*10, "\n", f, "\n", "-"*10)
                min_cut.append(None)
                max_cut.append(None)
                try:
                    measure_obj, is_created = model_measure_dim.objects.get_or_create(measure_group_dim=group_obj,
                                                                                      measure_name=f_)
                    if is_created:
                        measure_obj.measure_code = f_
                        measure_obj.save()
                except Exception as ex:
                    print("Error 90121-300", ex)
                for index, row in df.iterrows():
                    # print(row)
                    if row[1] is not None and str(row[1]) != "None" and str(row[1]) != "":
                        n_ = 0
                        entity_id = str(row[1]).strip()
                        entity_serial = int(str(row[2]).strip())
                        entity_race = int(str(row[3]).strip())
                        # print("=" * 50)
                        s_ = str(row[1]).lower()
                        if s_ == "min_cut" or s_ == "max_cut":
                            pass
                            # print(columns[j])
                            # try:
                            #     if s_ == "min_cut":
                            #         # print("Min_Cut", row[columns[j]])
                            #         min_cut[j] = float(row[columns[j]])
                            #     if s_ == "max_cut":
                            #         # print("Max_Cut", row[columns[j]])
                            #         max_cut[j] = float(row[columns[j]])
                            #     if min_cut[j] is not None and max_cut[j] is not None:
                            #         # print(f + str(n_), columns[j], "=", min_cut[j], max_cut[j])
                            #         try:
                            #             min_max_cut_obj, is_created = model_min_max_cut.objects.get_or_create(time_dim=year_obj,
                            #                                                                                   measure_dim=measure_obj)
                            #             if is_created:
                            #                 min_max_cut_obj.min = min_cut[j]
                            #                 min_max_cut_obj.max = max_cut[j]
                            #                 min_max_cut_obj.save()
                            #         except Exception as ex:
                            #             pass
                            # except Exception as ex:
                            #     print(ex)
                        else:
                            try:
                                # print(entity_id)
                                entity_dim_obj, is_created = model_entity_dim.objects.get_or_create(entity_id=entity_id)
                                if is_created:
                                    entity_dim_obj.entity_serial = entity_serial
                                    entity_dim_obj.entity_race = entity_race
                                    entity_dim_obj.save()
                            except Exception as ex:
                                print("Error 90121-400", ex)
                            try:
                                v_ = float(str(row[f_]))
                                if v_ is not None and str(v_) != "nan":
                                    # print(row[columns[j]], float(str(row[columns[j]])))
                                    fact_obj, is_created = model_fact.objects.get_or_create(entity_dim=entity_dim_obj,
                                                                                            measure_dim=measure_obj)
                                    fact_obj.amount = v_
                                    fact_obj.save()
                            except Exception as ex:
                                print("Error 90121-500", ex)

        wb.close()
        result = {"status": "ok"}
        # print(result)

        return result

