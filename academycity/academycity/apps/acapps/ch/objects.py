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

from django.contrib.auth.models import User, Group

class ChAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 ChAlgo\n", dic, '\n', '-'*50)
        try:
            super(ChAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 ChDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("AvicAlgo\n", self.app)
        # print("90004-020 ChAlgo\n", dic, '\n', '-'*50)
        self.app = dic["app"]
        # print("ChAlgo 9004", self.app)
        measure_group_model_name_ = dic["measure_group_model"]
        self.model_measure_group = apps.get_model(app_label=self.app, model_name=measure_group_model_name_)


class ChDataProcessing(BaseDataProcessing, BasePotentialAlgo, ChAlgo):
    def __init__(self, dic):
        # print("90005-000 AvicDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 AvicDataProcessing ", self.app)

    def upload_branches(self, dic):
        print('90100-1000-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print("-"*100, "\n", file_path, "\n", "-"*100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        #
        model_members = apps.get_model(app_label=app_, model_name="members")
        model_branches = apps.get_model(app_label=app_, model_name="branches")
        #
        my_group, is_created = Group.objects.get_or_create(name='c_admin')

        n_ = 100
        for index, row in df.iterrows():
            n_ += 1
            branch_name_ = str(row["branch_name"]).upper()
            username_ = str(row["username"])
            password_ = str(row["password"])

            email_ = str(row["email"])
            if email_ == "":
                email_ = username_+'@gmail.com'

            branch_leader_ = str(row["branch_leader"])

            l = branch_leader_.split(" ")
            print(l)
            suffix_ = l[0]
            first_name_ = l[1]
            last_name_ = l[2]

            try:
                u = User.objects.get(username=username_)
                count = u.delete()
                # print("B count\n", count, "\n")
            except Exception as ex:
                # pass
                print("9055-55 Error " + str(ex))
            try:
                u = User.objects.create_user(username=username_, email=email_, password=password_)
                # print(u.password)
                u.first_name = first_name_
                u.last_name = last_name_
                u.save()
                my_group.user_set.add(u)
                my_group.save()
            except Exception as ex:
                print("9000-00 Error " + str(ex))

            try:
                member_obj, is_created = model_members.objects.get_or_create(user=u)
                member_obj.first_name = first_name_
                member_obj.last_name = last_name_
                member_obj.suffix = suffix_
                member_obj.save()
            except Exception as ex:
                print("9001-01 Error " + str(ex))

            try:
                branch_obj, is_created = model_branches.objects.get_or_create(name=branch_name_, branch_leader=member_obj)
                branch_obj.name = branch_name_
                branch_obj.save()
                member_obj.branch = branch_obj
                member_obj.save()
            except Exception as ex:
                print("9001-02 Error " + str(ex))

        print("Done")
        result = {"status": "ok"}
        return result

    def upload_cells(self, dic):
        print('90100-1000-2 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print("-"*100, "\n", file_path, "\n", "-"*100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)

        n_cell = 100
        n_name = 100
        for index, row in df.iterrows():
            branch_ = str(row["branch"])
            if branch_ != "Kampala":
                continue
            cell_code_ = str(row["cell_code"])
            if cell_code_ == "" or cell_code_ == "nan":
                n_cell += 1
                cell_code_ = "MISS" + str(n_cell)
            # print(cell_code_)

            cell_name_ = str(row["cell_name"])
            if cell_name_ == "" or cell_name_ == "nan":
                n_name += 1
                cell_name_ = "MISS" + str(n_name)
            else:
                cell_name_ = cell_name_.replace("CELL", "").strip()
            # print(cell_name_)

            location_ = str(row["location"])
            cell_leader_ = str(row["cell_leader"]).strip()
            l = cell_leader_.split(" ")
            len_ = len(l)
            last_name_ = ""
            first_name_ = ""
            try:
                last_name_ = l[0]
                first_name_ = l[1]
            except Exception as ex:
                pass

            # if len_ > 2:
            #     print(len_)
            #     print(last_name_, first_name_)

            try:
                u = User.objects.get(first_name=first_name_, last_name = last_name_)
                print(u)
            except Exception as ex:
                print(ex)




        #
        # model_members = apps.get_model(app_label=app_, model_name="members")
        # model_branches = apps.get_model(app_label=app_, model_name="branches")
        # #
        # my_group, is_created = Group.objects.get_or_create(name='c_admin')
        #
        # n_ = 100
        # for index, row in df.iterrows():
        #     n_ += 1
        #     branch_name_ = str(row["branch_name"]).upper()
        #     username_ = str(row["username"])
        #     password_ = str(row["password"])
        #
        #     email_ = str(row["email"])
        #     if email_ == "":
        #         email_ = username_+'@gmail.com'
        #
        #     branch_leader_ = str(row["branch_leader"])
        #
        #     l = branch_leader_.split(" ")
        #     print(l)
        #     suffix_ = l[0]
        #     first_name_ = l[1]
        #     last_name_ = l[2]
        #
        #     try:
        #         u = User.objects.get(username=username_)
        #         count = u.delete()
        #         # print("B count\n", count, "\n")
        #     except Exception as ex:
        #         # pass
        #         print("9055-55 Error " + str(ex))
        #     try:
        #         u = User.objects.create_user(username=username_, email=email_, password=password_)
        #         # print(u.password)
        #         u.first_name = first_name_
        #         u.last_name = last_name_
        #         u.save()
        #         my_group.user_set.add(u)
        #         my_group.save()
        #     except Exception as ex:
        #         print("9000-00 Error " + str(ex))
        #
        #     try:
        #         member_obj, is_created = model_members.objects.get_or_create(user=u)
        #         member_obj.first_name = first_name_
        #         member_obj.last_name = last_name_
        #         member_obj.suffix = suffix_
        #         member_obj.save()
        #     except Exception as ex:
        #         print("9001-01 Error " + str(ex))
        #
        #     try:
        #         branch_obj, is_created = model_branches.objects.get_or_create(name=branch_name_, branch_leader=member_obj)
        #         branch_obj.name = branch_name_
        #         branch_obj.save()
        #         member_obj.branch = branch_obj
        #         member_obj.save()
        #     except Exception as ex:
        #         print("9001-02 Error " + str(ex))

        print("Done")
        result = {"status": "ok"}
        return result


