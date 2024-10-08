import numpy as np
import json
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import seaborn as sns
from tensorboard.plugins.image.summary import image
from twisted.words.protocols.jabber.error import exceptionFromStreamError

# -----
from ..basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
# -----
from abc import ABC, abstractmethod

class AbstractModels(ABC):
    def __init__(self, dic):
        # print("AbstractModels\n", dic)
        try:
            self.datadir = dic['datadir']
        except Exception as ex:
            print("Error 20-01", ex, "need to provide dir name")
            self.datadir = ""
        try:
            self.model_name = dic['model_name']
        except Exception as ex:
            print("Error 20-02", ex, "need to provide model name")
            self.model_name = "General_name"
        self.checkpoint_file = os.path.join(self.datadir, "checkpoint_"+self.model_name+"_wt")
        self.model = None

    @abstractmethod
    def get_data(self, **data):
        pass

    @abstractmethod
    def normalize_data(self, **data):
        pass

    @abstractmethod
    def get_model(self):
        pass

    def save(self):
        tf.keras.models.save_model(self.model, self.checkpoint_file, overwrite=True)

    def checkpoint_model(self):
        if not os.path.exists(self.checkpoint_file):
            self.model.predict(np.ones((20, 28, 28), dtype=np.float32))
            self.save()
        else:
            self.model = tf.keras.models.load_model(self.checkpoint_file)

class History(object):
   def __init__(self):
    self.history = {}
    self.epoch = None

class FashionMNistClassify(AbstractModels, ABC):
    def __init__(self, dic) -> None:
        # print("A FashionMNistClassify\n", dic)
        super(FashionMNistClassify, self).__init__(dic)
        # print("B FashionMNistClassify\n", dic)
        self.dic = dic
        useGradTape = False
        self.trainingData = None
        self.testingData = None
        # ---
        self.get_data()
        # print(self.trainingData[0][0])
        # ---
        self.classes = ["Top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Boot"]
        self.nClass = len(self.classes)
        # ---
        self.batchSize = int(dic["batchsize"])
        self.nEpoch = int(dic["epochs"])
        self.useGradientTape = useGradTape
        # ---
        self.loss = None
        self.optimizer = None
        self.metric = None
        # ---
        self.model = None
        self.get_model()
        # ---

    def get_data(self, **data):
        (trainx, trainy), (testx, testy) = tf.keras.datasets.fashion_mnist.load_data()
        # ---
        trainx, testx = self.normalize_data(trainx=trainx, testx=testx)
        # ---
        self.trainingData = (trainx, trainy)
        self.testingData = (testx, testy)

    def save_images(self):
        # Directory to save images
        image_dir = self.dic["imagesdir"]
        n_images = int(self.dic["n_images"])
        image_ext = "/media" + image_dir.split("media")[1]+"/"
        # print("ext", image_ext)
        image_urls = {}
        for class_idx in range(10):
            class_name = self.classes[class_idx]
            # print(class_name)
            image_urls[class_name] = {}
            # idx = np.where(self.trainingData[1] == class_idx)[0][n_images]
            indices = np.where(self.trainingData[1] == class_idx)[0][:n_images]
            for i, idx in enumerate(indices):
                image = self.trainingData[0][idx]
                # image_path = os.path.join(image_dir, f'{class_name}.png')
                image_path = os.path.join(image_dir, f'{class_name}_{i}.png')
                image_urls[class_name][i] = image_ext+class_name+"_"+str(i)+'.png'
                plt.imsave(image_path, image, cmap='gray')
        return image_urls

    def normalize_data(self, **data):
        trainx = data["trainx"]
        testx = data["testx"]
        trainx = trainx/255.0
        testx = testx/255.0
        return trainx, testx

    def get_model(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
        self.model.add(tf.keras.layers.Dense(80,activation="relu"))
        self.model.add(tf.keras.layers.Dense(20, activation="relu"))
        self.model.add(tf.keras.layers.Dense(10))
        # ---None
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.005)
        self.metric = tf.keras.metrics.SparseCategoricalAccuracy()
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=[self.metric])
        # ---
        self.checkpoint_model()
        # ---

    def getConfusionMatrix(self, labels: np.ndarray,predictions: np.ndarray):
        predictedLabels = np.argmax(predictions, axis=1)
        # fig, ax = plt.subplots()
        cm = np.zeros((self.nClass, self.nClass),dtype=np.int32)
        for i in range(labels.shape[0]):
            cm[labels[i], predictedLabels[i]] += 1
        return cm

    def plotConvergenceHistory(self, history, metricName):
        # print(metricName)
        # print(history.epoch, history.history[metricName])
        return {"x": history.epoch, "y": history.history[metricName]}

    def testModel(self):
        dic = {}
        n = 0
        ds = ["train", "test"]
        for X, y in [self.trainingData, self.testingData]:
            predictClass = self.model.predict(X)
            cm = self.getConfusionMatrix(y, predictClass)
            dic[ds[n]] = cm
            n +=1
        return dic

    def gradTapeTraining(self):
        trainDataset = tf.data.Dataset.from_tensor_slices(self.trainingData)
        trainDataset = trainDataset.batch(self.batchSize)
        totalLoss = np.zeros(self.nEpoch, dtype=np.float32)
        count = 0
        for X, y in trainDataset:
            for epoch in range(self.nEpoch):
                with tf.GradientTape() as tape:
                    predictedY = self.model(X)
                    loss = self.loss(y, predictedY)
                    # print("y\n", y, "\npredictY\n", predictedY)
                grads = tape.gradient(loss, self.model.trainable_weights)
                # print("Epoch", epoch)
                # print("loss", loss)
                totalLoss[epoch] += loss
                # print(totalLoss)
                self.optimizer.apply_gradients(zip(grads,self.model.trainable_weights))
            count += 1
        totalLoss = totalLoss / count
        history = History()
        history.history["loss"] = totalLoss
        history.history[self.metric._name] = np.zeros(self.nEpoch)
        history.epoch = np.arange(self.nEpoch)
        return history

    def trainModel(self):
        if self.useGradientTape:
            history = self.gradTapeTraining()
        else:
            try:
                history = self.model.fit(self.trainingData[0], self.trainingData[1],
                                        batch_size = self.batchSize,
                                        epochs = self.nEpoch)
                self.save()
            except Exception as ex:
                print("Error 22-22-3", ex)

        dic = {}
        dic[self.metric._name] = self.plotConvergenceHistory(history, self.metric._name)
        dic["loss"] = self.plotConvergenceHistory(history, "loss")
        return dic

class SNNAlgo(object):
    def __init__(self, dic):
        # print("90567-8-000 Algo\n", dic, '\n', '-'*50)
        try:
            super(SNNAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 Algo:\n" + str(ex), "\n", '-' * 50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 Algo\n", dic, '\n', '-'*50)
        self.app = dic["app"]

# https://chatgpt.com/c/66e0947c-6714-800c-9probabilitiesef3-3aa45026ed5a
class SNNDataProcessing(BaseDataProcessing, BasePotentialAlgo, SNNAlgo):
    def __init__(self, dic):
        print("908889-010 SNNDataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.MODELS_PATH = os.path.join(self.TO_OTHER, "models")
        os.makedirs(self.MODELS_PATH, exist_ok=True)
        # print(self.MODELS_PATH)
        # -----
        self.SCALER_PATH = os.path.join(self.TO_OTHER, "scalers")
        os.makedirs(self.SCALER_PATH, exist_ok=True)
        # -----
        self.IMAGES_PATH = os.path.join(self.TO_MEDIA, "images")
        os.makedirs(self.IMAGES_PATH, exist_ok=True)
        # print(self.IMAGES_PATH)

    def get_images(self, dic):
        print("\n90448-SNN get_images: \n", "=" * 50, "\n", dic, "\n", "=" * 50)
        # Load stock data using Yahoo Finance
        # ticker = dic["ticker"]
        # ---------------
        # print(self.IMAGES_PATH)
        dic = {"n_images":int(dic["n_images"]) ,"imagesdir": self.IMAGES_PATH, "datadir": self.MODELS_PATH,
               "model_name": "FashionMNistClassify", "batchsize": 10000, "epochs": 60}
        fmnist = FashionMNistClassify(dic)

        image_urls = fmnist.save_images()  # Save the images
        # print(image_urls)
        # image_urls = {class_name: f'/media/fashion_mnist/{class_name}.png' for class_name in class_names}
        # print(image_urls)

        result = {"status": "ok", "image_urls": image_urls}
        return result

    def train(self, dic):
        print("\n90445-SNN train: \n", "=" * 50, "\n", dic, "\n", "=" * 50)
        # Load stock data using Yahoo Finance
        # ticker = dic["ticker"]
        # ---------------
        dic = {"datadir": self.MODELS_PATH, "model_name": "FashionMNistClassify", "batchsize": 10000, "epochs": 60}
        fmnist = FashionMNistClassify(dic)
        # fmnist = FashionMNistClassify(dname, batchsize=10000, epochs=60)

        charts = fmnist.trainModel()
        for k in charts:
            charts[k]["y"] = [round(100*x)/100 for x in charts[k]["y"]]
        print(charts)

        result = {"status": "ok", "charts": charts}
        return result

    def test(self, dic):
        print("90444-SNN: \n", "=" * 50, "\n", dic, "\n", "=" * 50)
        # ticker = dic["ticker"]
        dic = {"datadir": self.MODELS_PATH, "model_name": "FashionMNistClassify", "batchsize": 10000, "epochs": 60}
        fmnist = FashionMNistClassify(dic)
        cms = fmnist.testModel()
        for cm in cms:
            cms[cm] = eval(json.dumps(cms[cm].tolist()))
        result = {"status": "ok", "cms":cms, "classes":fmnist.classes}

        # print(result)

        return result
