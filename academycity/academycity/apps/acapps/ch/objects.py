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


class AvicDataProcessing(BaseDataProcessing, BasePotentialAlgo, ChAlgo):
    def __init__(self, dic):
        # print("90005-000 AvicDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 AvicDataProcessing ", self.app)


