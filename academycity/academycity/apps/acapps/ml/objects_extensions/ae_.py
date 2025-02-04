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
from .ae_simple import AES
from .ae_vae import VAEDP
from .ae_dae import DVADP
#


class AEAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90561-8-010 Algo\n", dic, '\n', '-'*50)
        try:
            super(AEAlgo, self).__init__()
        except Exception as ex:
            print("Error AE 9057-010 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class AEDataProcessing(BaseDataProcessing, BasePotentialAlgo, AEAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.PATH = os.path.join(self.TO_OTHER, "ae")
        os.makedirs(self.PATH, exist_ok=True)
        # print(f'{self.PATH}')
        clear_log_debug()
        #

    # For Simple one independent variable.
    def activate(self, dic):
        print("90155-ae-1: \n", "="*50, "\n", dic, "\n", "="*50)
        # epochs = int(dic["epochs"])
        o = dic["obj"]
        f = dic["obj_fun"]
        s = o+"(dic)."+f+"(dic)"
        print(s)
        result = eval(o+"(dic)."+f+"(dic)")
        print(result)
        return result


