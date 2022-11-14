import warnings
import os
from django.conf import settings
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
from openpyxl import Workbook, load_workbook
import pandas as pd
#
from .models import TimeDim, CountryDim, WorldBankFact
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


class BaseDataProcessing(object):
    def __init__(self, dic):   # to_data_path, target_field
        self.name = 'DataProcessing'
        # print('-'*50)
        # print('9001 in constructor parent')
        # print('-'*50)
        warnings.filterwarnings(action="ignore", message="^internal gelsd")
        # to make this notebook's output stable across runs

        self.RANDOM_STATE = 42
        np.random.seed(self.RANDOM_STATE)

        # To plot pretty figures
        mpl.rc('axes', labelsize=14)
        mpl.rc('xtick', labelsize=12)
        mpl.rc('ytick', labelsize=12)
        # Where to save the figures
        # --- Change to this when you start to use Django ---
        self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", "avi")

        # print(self.PROJECT_ROOT_DIR)
        # print('-'*50)

        os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)

        self.TOPIC_ID = dic["topic_id"]  # "fundamentals"
        self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
        os.makedirs(self.TO_DATA_PATH, exist_ok=True)
        self.TO_EXCEL = os.path.join(self.TO_DATA_PATH, "excel", self.TOPIC_ID)
        os.makedirs(self.TO_EXCEL, exist_ok=True)
        self.IMAGES_PATH = os.path.join(self.PROJECT_ROOT_DIR, "images", self.TOPIC_ID)
        os.makedirs(self.IMAGES_PATH, exist_ok=True)
        self.MODELS_PATH = os.path.join(self.PROJECT_ROOT_DIR, "models", self.TOPIC_ID)
        os.makedirs(self.MODELS_PATH, exist_ok=True)

        # self.TARGET_FIELD = target_field
        # self.DATA = None
        # self.TRAIN = None
        # self.TEST = None
        # self.TRAIN_TARGET = None
        # self.TRAIN_DATA = None
        # self.TEST_TARGET = None
        # self.TEST_DATA = None
        # self.train_data = None
        # self.test_data = None
        # self.num_attribs = None
        # self.extra_attribs = None
        # self.model = None
        # self.HASH = hashlib.md5
        # self.PIPELINE = None

        # print('-'*50)
        # print('9010 - End constructor parent')
        # print('-'*50)

    def upload_file(self, dic):
        # print("avi upload_file:")
        # print(dic)
        # print("avi upload_file:")
        upload_file_ = dic["request"].FILES['drive_file']
        result = {}
        # We can extend and add another property: data_folder
        # like topic_id. But, we need to add this property to: params in the core view
        # and use it here.
        # for example: if data_folder=excel we choose self.TO_EXCEL

        # print("target_folder = self.TO_"+dic["folder_type"].upper())
        target_folder = eval("self.TO_"+dic["folder_type"].upper())

        filename = dic["request"].POST['filename']
        file_path = os.path.join(target_folder, filename)
        with open(file_path, 'wb+') as destination:
            for c in upload_file_.chunks():
                destination.write(c)

        # print("9017\nUploaded\n", "-" * 30)
        load_dic = {"file_path": file_path}
        self.load_file_to_db(load_dic)
        result['file_remote_path'] = file_path
        return result


class DataProcessing(BaseDataProcessing):
    def __init__(self, dic):
        super().__init__(dic)

    def load_file_to_db(self, dic):
        file_path = dic["file_path"]
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)
        print(df.columns)

        result = {"status": "ok"}
        return result
