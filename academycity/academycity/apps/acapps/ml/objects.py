import warnings
import os
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
import matplotlib.pyplot as plt

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
#
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, SimpleRNN
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.datasets import mnist
#
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten
#

class MLAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000 MLAlgo\n", dic, '\n', '-'*50)
        try:
            super(MLAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 MLDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 MLAlgo\n", dic, '\n', '-'*50)
        self.app = dic["app"]


class MLDataProcessing(BaseDataProcessing, BasePotentialAlgo, MLAlgo):
    def __init__(self, dic):
        # print("90005-000 MLDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 MLDataProcessing ", self.app)


    # _1  I adjusted this function to work after uploading Eli data
    def mlp(self, dic):
        # print("90121-5: \n", "="*50, "\n", dic, "\n", "="*50)
        # load mnist dataset
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        # compute the number of labels
        num_labels = len(np.unique(y_train))
        # convert to one-hot vector
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        # image dimensions (assumed square)
        image_size = x_train.shape[1]
        input_size = image_size * image_size
        # resize and normalize
        x_train = np.reshape(x_train, [-1, input_size])
        x_train = x_train.astype('float32') / 255
        x_test = np.reshape(x_test, [-1, input_size])
        x_test = x_test.astype('float32') / 255
        # network parameters
        batch_size = 128
        hidden_units = 256
        dropout = 0.45
        # model is a 3-layer MLP with ReLU and dropout after each layer
        model = Sequential()
        model.add(Dense(hidden_units, input_dim=input_size))
        model.add(Activation('relu'))
        model.add(Dropout(dropout))
        model.add(Dense(hidden_units))
        model.add(Activation('relu'))
        model.add(Dropout(dropout))
        model.add(Dense(num_labels))
        # this is the output for one-hot vector
        model.add(Activation('softmax'))
        print("model.summary()")
        model.summary()
        # file_path = os.path.join(self.PICKLE_PATH, "mlp-mnist.png")
        # plot_model(model, to_file=file_path, show_shapes=True)
        # loss function for one-hot vector
        # use of adam optimizer
        # accuracy is good metric for classification tasks
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        # train the network
        model.fit(x_train, y_train, epochs=20, batch_size=batch_size)
        # validate the model on test dataset to determine generalization
        _, acc = model.evaluate(x_test,
                                y_test,
                                batch_size=batch_size,
                                verbose=0)
        print("\nTest accuracy: %.1f%%" % (100.0 * acc))

        result = {"status": "ok"}
        return result

    def cnn(self, dic):
        print("90122-TEST1: \n", "="*50, "\n", dic, "\n", "="*50)
        # load mnist dataset
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        # compute the number of labels
        num_labels = len(np.unique(y_train))
        # convert to one-hot vector
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        # input image dimensions
        image_size = x_train.shape[1]
        # resize and normalize
        x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
        x_test = np.reshape(x_test, [-1, image_size, image_size, 1])
        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255
        # network parameters
        # image is processed as is (square grayscale)
        input_shape = (image_size, image_size, 1)
        batch_size = 128
        kernel_size = 3
        pool_size = 2
        filters = 64
        dropout = 0.2
        # model is a stack of CNN-ReLU-MaxPooling
        model = Sequential()
        model.add(Conv2D(filters=filters,
                         kernel_size=kernel_size,
                         activation='relu',
                         input_shape=input_shape))
        model.add(MaxPooling2D(pool_size))
        model.add(Conv2D(filters=filters,
                         kernel_size=kernel_size,
                         activation='relu'))
        model.add(MaxPooling2D(pool_size))
        model.add(Conv2D(filters=filters,
                         kernel_size=kernel_size,
                         activation='relu'))
        model.add(Flatten())
        # dropout added as regularizer
        model.add(Dropout(dropout))
        # output layer is 10-dim one-hot vector
        model.add(Dense(num_labels))
        model.add(Activation('softmax'))
        model.summary()
        # plot_model(model, to_file='cnn-mnist.png', show_shapes=True)
        # loss function for one-hot vector
        # use of adam optimizer
        # accuracy is good metric for classification tasks
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        # train the network
        model.fit(x_train, y_train, epochs=10, batch_size=batch_size)
        _, acc = model.evaluate(x_test,
                                y_test,
                                batch_size=batch_size,
                                verbose=0)
        print("\nTest accuracy: %.1f%%" % (100.0 * acc))

        result = {"status": "ok CNN"}
        return result

    def rnn(self, dic):
        print("90122-TEST1: \n", "="*50, "\n", dic, "\n", "="*50)
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        # compute the number of labels
        num_labels = len(np.unique(y_train))
        # convert to one-hot vector
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        # resize and normalize
        image_size = x_train.shape[1]
        x_train = np.reshape(x_train, [-1, image_size, image_size])
        x_test = np.reshape(x_test, [-1, image_size, image_size])
        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255
        # network parameters
        input_shape = (image_size, image_size)
        batch_size = 128
        units = 256
        dropout = 0.2
        # model is RNN with 256 units, input is 28-dim vector 28 timesteps
        model = Sequential()
        model.add(SimpleRNN(units=units,
                            dropout=dropout,
                            input_shape=input_shape))
        model.add(Dense(num_labels))
        model.add(Activation('softmax'))
        model.summary()
        # plot_model(model, to_file='rnn-mnist.png', show_shapes=True)
        # loss function for one-hot vector
        # use of sgd optimizer
        # accuracy is good metric for classification tasks
        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])
        # train the network
        model.fit(x_train, y_train, epochs=20, batch_size=batch_size)
        _, acc = model.evaluate(x_test,
                                y_test,
                                batch_size=batch_size,
                                verbose=0)
        print("\nTest accuracy: %.1f%%" % (100.0 * acc))

        result = {"status": "ok RNN", "acc": acc}
        return result




class Algo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90040-000 MLAlgo\n", dic, '\n', '-'*50)
        try:
            super(Algo, self).__init__()
        except Exception as ex:
            print("Error 90004-010 Algo:\n"+str(ex), "\n", '-'*50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 Algo\n", dic, '\n', '-'*50)
        self.app = dic["app"]

class MLAlgo(BaseDataProcessing, BasePotentialAlgo, Algo):
    def __init__(self, dic):
        print("90050-000 MLDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 MLAlgo ", self.app)


    def algo_test(self, dic):
        print("90121-5: \n", "="*50, "\n", dic, "\n", "="*50)


        output = {"numbers":[1,2,3,4,5]}
        result = {"status": "ok", "output":output}
        return result

