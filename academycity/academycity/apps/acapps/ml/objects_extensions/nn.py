from ..basic_ml_objects import BaseDataProcessing, BasePotentialAlgo

from ....core.utils import log_debug, clear_log_debug

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import random
import gym
import numpy as np
from collections import deque
import pickle

from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.optimizers import Adam, RMSprop

import tensorflow as tf
from tensorflow.keras import layers, models, initializers, optimizers


class NNAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90567-8-000 Algo\n", dic, '\n', '-'*50)
        try:
            super(NNAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class NNDataProcessing(BaseDataProcessing, BasePotentialAlgo, NNAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.PATH = os.path.join(self.TO_OTHER, "nn")
        os.makedirs(self.PATH, exist_ok=True)
        # print(f'{self.PATH}')
        self.model = None
        self.lose_list = None

    def load(self, name):
        self.model = load_model(name)

    def save(self, file_name):
        self.model.save(file_name)

    def train(self, dic):
        print("90155-nn: \n", "="*50, "\n", dic, "\n", "="*50)
        epochs = int(dic["epochs"])
        continue_train = int(dic["continue_train"])
        data_only = int(dic["data_only"])
        a_ = float(dic["a"])
        b_ = float(dic["b"])
        num_samples_ = int(dic["num_samples"])
        sigma_ = float(dic["sigma"])

        # Generate sample data
        def generate_data(num_samples=1500, true_a=25.0, true_b=0.7, sigma=20):
            X = np.random.uniform(0, 1, num_samples)*300
            Y = true_a + true_b * X + np.random.normal(0, sigma, num_samples)
            return X, Y

        def create_model():
            model = models.Sequential()
            model.add(layers.Dense(1, input_shape=(1,), activation='linear'
            #                        kernel_initializer=initializers.Zeros(),
            #                        bias_initializer=initializers.Zeros())
                                   ))  # One neuron, linear activation
            model.compile(optimizer='adam', loss='mean_squared_error')
            # model.compile(optimizer='RMSprop', loss='mean_squared_error')
            return model

        # Generate data
        X_train, Y_train = generate_data(num_samples=num_samples_,true_a=a_, true_b=b_,sigma=sigma_)

        if data_only == 1:
            result = {"status": "ok nn", "data": {"x": X_train.tolist(), "y": Y_train.tolist(),
                                                  "a": 0, "b": 0}}
            return result

        model_path = f'{self.PATH}/pickles/{"nn.pkl"}'
        model_path_l = f'{self.PATH}/pickles/{"nn_lose.pkl"}'
        # print(model_path)

        if model_path and os.path.exists(model_path) and continue_train==1:
            print(f"Loading model from {model_path}")
            self.model = load_model(model_path)
            if model_path_l and os.path.exists(model_path_l):
                with open(model_path_l, 'rb') as file:
                    self.lose_list = pickle.load(file)
        else:
            print("Creating new model")
            self.model = create_model()
            self.lose_list = []

        history = self.model.fit(X_train, Y_train, epochs=epochs, verbose=1)
        self.save(model_path)

        loss_values = history.history['loss']
        for k in range(len(loss_values)):
            if (k++1) % 100 == 0:
                self.lose_list.append(loss_values[k])

        # print("self\n", self.lose_list)

        with open(model_path_l, 'wb') as file:
            pickle.dump(self.lose_list, file)

        # Extract the learned parameters (a and b)
        weights = self.model.get_weights()
        # print(weights)

        learned_b = round(100*weights[0][0][0])/100  # Slope (b)
        learned_a = round(100*weights[1][0])/100  # Intercept (a)

        # print(f"Learned parameters: a = {learned_a}, b = {learned_b}")

        result = {"status": "ok nn", "data":{"x":X_train.tolist(), "y":Y_train.tolist(),
                                             "a": learned_a, "b": learned_b,
                                             "loss_values": self.lose_list}}

        return result

