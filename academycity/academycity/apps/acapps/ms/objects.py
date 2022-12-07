import warnings
import os
from django.conf import settings
from ..ml.basic_ml_objects import BaseDataProcessing
import matplotlib as mpl
from django.apps import apps

import sys
import shutil
import pandas as pd
import numpy as np
import math
from openpyxl.utils.dataframe import dataframe_to_rows
import csv
import pickle
from concurrent.futures import ThreadPoolExecutor as T
from openpyxl import Workbook, load_workbook

mpl.use('Agg')


class MSDataProcessing(BaseDataProcessing):
    def __init__(self, dic):
        super().__init__(dic)

    def get_general_data(self, dic):
        # print("DataProcessing get_general_data 9012:\n")
        # print(dic)
        app_ = dic["app"]

        # dic = {"app": "avi",
        #        "dimensions": {"time_dim": {"model": "TimeDim", "field_name": "year"},
        #                       "country_dim": {"model": "CountryDim", "field_name": "country_name"} }}

        result = {}
        for k in dic["dimensions"]:
            dic_ = dic["dimensions"][k]
            s = k + ' = {}'
            try:
                exec(s)
                # print(eval(k))
                model_name_ = dic["dimensions"][k]["model"]
                # print(model_name_)
                model_ = apps.get_model(app_label=app_, model_name=model_name_)
                # print(model_)
                for r in model_.objects.all():
                    # print(r)
                    s = k + '["'+str(r.id)+'"] = r.' + dic["dimensions"][k]["field_name"]
                    # print(s)
                    exec(s)
                # print(eval(k))
            except Exception as ex:
                print("err 1000: " + str(ex))

            # print('result[k] = ' + k)
            exec('result[k] = ' + k)
        # print(result)
        return result

    def load_file_to_db(self, dic):
        print("90121-1: \n", dic, "="*50)
        print(dic)
        print('dic')
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # file_path = "/home/amos/projects/development/academycity/data/ms/datasets/excel/raw_data/RAW DATA (607).xlsx"
        # print('file_path')
        # print(file_path)
        # print('file_path')

        print('90121-2 dic')
        dic = dic["cube_dic"]
        print('90121-3 dic', dic)
        model_name_ = dic["dimensions"]["person_dim"]["model"]
        print(model_name_)
        model_person_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["dimensions"]["gene_dim"]["model"]
        print(model_name_)
        model_gene_dim = apps.get_model(app_label=app_, model_name=model_name_)

        model_name_ = dic["fact"]["model"]
        print(model_name_)
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        print('90121-4 fact')

        wb = load_workbook(filename=file_path, read_only=False)
        sheet_names = wb.sheetnames
        f = "RAW DATA (607)"
        ws = wb[f]
        data = ws.values
        # Get the first line in file as a header line
        columns = next(data)[0:]
        # print(columns)
        # Create a DataFrame based on the second and subsequent lines of data
        df = pd.DataFrame(data, columns=columns)
        df = df.reset_index()  # make sure indexes pair with number of rows
        # print(df)
        max_v = 0
        max_d = 0
        n__ = 0
        for index, row in df.iterrows():
            n__ += 1
            if 8990 < n__ < 10000:
                for j in range(1, len(columns)):
                    if row[1] is not None and str(row[1]) != "None" and str(row[1]) != "":
                        g_ = str(row[1])
                        gene_dim_obj, is_created = model_gene_dim.objects.get_or_create(gene_code=g_)
                        p_ = str(columns[j])
                        if p_ != "None" and p_ != "":
                            # print("p_", p_)
                            person_dim_obj, is_created = model_person_dim.objects.get_or_create(person_code=p_)
                        try:
                            v_ = float(str(row[columns[j]]))
                            if (v_ <= -0.000001) or (v_ > 0.000001):
                                if max_v < v_:
                                    max_v = v_
                                v_ = str(v_).split(".")[1]
                                if int(v_) > max_d:
                                    max_d = int(v_)
                                fact_obj, is_created = model_fact.objects.get_or_create(gene_dim=gene_dim_obj,
                                                                                        person_dim=person_dim_obj)
                                fact_obj.amount = v_
                                fact_obj.save()
                        except Exception as ex:
                            print("Error 9055-33: "+str(ex))

            # print(f_, p_, v_)
            print(n__, max_v, max_d)
        print(max_v, max_d)
        wb.close()
        result = {"status": "ok"}
        return result
