import os

from twisted.mail.smtp import xtext_codec

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
from datetime import datetime
import pickle

from keras.models import Model, load_model
from keras.optimizers import Adam, RMSprop
import tensorflow as tf
from tensorflow.keras import layers, models, initializers, optimizers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#
from ..basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from ....core.utils import log_debug, clear_log_debug
#
from ....core.utils import log_debug, clear_log_debug
#


class AESAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90561-8-010-3 Algo\n", dic, '\n', '-'*50)
        try:
            super(AESAlgo, self).__init__()
        except Exception as ex:
            print("Error AES 9057-010-9 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class AES(BaseDataProcessing, BasePotentialAlgo, AESAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.PATH = os.path.join(self.TO_OTHER, "aes")
        os.makedirs(self.PATH, exist_ok=True)
        # print(f'{self.PATH}')
        clear_log_debug()
        #

    # For Simple one independent variable.
    def train(self, dic):
        print("90155-aes-1: \n", "="*50, "\n", dic, "\n", "="*50)
        # epochs = int(dic["epochs"])


        result = {"status": "ok aes train", "data":{}}
        return result


