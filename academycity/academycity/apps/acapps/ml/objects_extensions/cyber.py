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
# --------------------------
import requests
import asyncio
import json
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
import pprint
# --------------------------


class CH6(object):
    def __init__(self, dic):
        # print("CH6\n", dic)
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

        log_debug("train_wb 110:" + self.checkpoint_file)

        # print(self.checkpoint_file)
        # ---
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        # ---
        self.model = None
        self.get_model()
        print("Obj creation - model was created")
        # ---
        self.trainData = None
        self.testData = None
        # =--
        self.history = None
        log_debug("train_wb 120:")

        print("End Obj creation")

    # --- Data ---
    def fetch_world_bank_data(self, countries, indicators):
        try:
            log_debug("train_wb 123-1: get_data.")
            # df = wbdata.get_dataframe(indicators, country=countries, date=("1980", "2024"), freq='Y')
            # Fetch data
            # countries = ['US', 'GB', 'CN']  # Example countries: United States, Great Britain, China
            df = wbdata.get_dataframe(indicators, country=countries, freq='Y')

            print(df)

            # Filter by date range (e.g., from 1980 to 2024)
            df = df[(df.index.get_level_values('date') >= datetime(1980, 1, 1)) &
                             (df.index.get_level_values('date') <= datetime(2024, 12, 31))]
        except Exception as ex:
            print("Err500-50-5", ex)
            log_debug("train_wb 123-2 Error: get_data." + str(ex))

        df.reset_index(inplace=True)
        # print("AAAdf\n\n", df)
        # Handle missing data
        # df.fillna(method='ffill', inplace=True)
        df = df.dropna()
        print("\n\nBBBBBdf\n\n", df)
        log_debug("train_wb 123-5: get_data.")
        return df

    def normalize_data(self, **data):
        trainx = data["trainx"]
        trainy = data["trainy"]
        testx = data["testx"]
        testy = data["testy"]
        # scale
        trainx = self.scaler_X.fit_transform(trainx)
        trainy = self.scaler_y.fit_transform(trainy).reshape(-1)

        # Transform the test data using the fitted scaler (no fitting here)
        testx = self.scaler_X.transform(testx)
        testy = self.scaler_y.transform(testy).reshape(-1)

        return (trainx, trainy), (testx, testy)

    def get_data(self, countries, indicators, dep_var, indep_var):

        df = self.fetch_world_bank_data(countries, indicators)

        log_debug("train_wb 125: data shape: " + str(df.shape))

        # Extract input features and target variable
        # print("\ndf from WB\n", df)
        X = df[indep_var].values
        y = df[dep_var].values.reshape(-1, 1)  # Reshape y for the scaler
        # print("X\n", X)
        # print("y\n", y)
        # Split data into training and testing sets

        # NEED TO CHECK SPLIT from random for testing to take only last records
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # print("X_train\n", X_train, "\nX_test", X_test)
        # print("y_train\n", y_train, "\ny_test", y_test)

        # Normalize the data
        self.trainData, self.testData = self.normalize_data(trainx=X_train, trainy=y_train, testx=X_test, testy=y_test)

        log_debug("train_wb 120: data normalized.")

        # print("\nAAtrain_data\n", train_data, "\nBBtest_data\n", test_data)

        self.trainData = tf.data.Dataset.from_tensor_slices((self.trainData[0], self.trainData[1]))
        self.trainData = self.trainData.batch(32).shuffle(buffer_size=1024).prefetch(tf.data.AUTOTUNE)
    # --- End Data ---

    # --- Model ---
    def save(self):
        tf.keras.models.save_model(self.model, self.checkpoint_file, overwrite=True)

    def checkpoint_model(self):
        if not os.path.exists(self.checkpoint_file):
            # self.model.predict(np.ones((20, 28, 28), dtype=np.float32))
            self.save()
        else:
            self.model = tf.keras.models.load_model(self.checkpoint_file)

    def get_model(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Dense(1, activation='linear', input_shape=(4, )))
        self.model.compile(optimizer='adam', loss='mse')
        # ---
        self.checkpoint_model()
        # ---
    # --- End Model ---

    def get_convergence_history(self, metric_name):
        # print(metric_name)
        # print(self.history.epoch, self.history.history[metric_name])
        y = self.history.history[metric_name]
        y = [round(1000*h)/1000 for h in y]
        return {"x": self.history.epoch, "y": y}

    def train(self, dic):
        countries = dic["countries"]  # Add any countries you want to analyze
        indicators = dic["indicators"]
        dep_var = dic["dep_var"]
        indep_var = dic["indep_var"]
        epochs_ = dic["epochs"]
        # ---
        log_debug("train_wb 122: got data.")

        self.get_data(countries, indicators, dep_var, indep_var)

        log_debug("train_wb 130: got data.")

        # print(self.trainData, "\n\n", self.testData)
        # ---
        self.history = self.model.fit(self.trainData, epochs=epochs_, batch_size=32, validation_data=self.testData)

        log_debug("train_wb 140: finished fit data.")

        matrices = {}
        for k in ["loss", "val_loss"]:
            matrices[k] = self.get_convergence_history(metric_name=k)
        # ---
        log_debug("train_wb 150: finished get_convergence_history.")
        # ---
        weights, biases = self.model.layers[0].get_weights()
        weights, biases = weights.reshape(-11).tolist(), biases.reshape(-1).tolist()
        weights = [round(1000*w)/1000 for w in weights]
        biases = [round(1000*b)/1000 for b in biases]
        # ---
        predictions = self.model.predict(self.testData[0])
        # ---
        log_debug("train_wb 160: finished model.predict.")
        # ---
        p = self.scaler_y.inverse_transform(predictions).reshape(-1).tolist()
        p = [round(x) for x in p]
        a = self.scaler_y.inverse_transform(self.testData[1].reshape(1, -1)).reshape(-1).tolist()
        a = [round(x) for x in a]
        ret = {"matrices":matrices, "a":a, "p": p, "weights":weights, "biases": biases}
        # print(ret)
        return ret


class CyberAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90567-8-000 Algo\n", dic, '\n', '-'*50)
        try:
            super(CyberAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 Algo:\n"+str(ex), "\n", '-'*50)

        self.app = dic["app"]


class CyberDataProcessing(BaseDataProcessing, BasePotentialAlgo, CyberAlgo):
    def __init__(self, dic):
        # print("90567-66010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)
        self.PATH = os.path.join(self.TO_OTHER, "cyber")
        os.makedirs(self.PATH, exist_ok=True)
        # print(f'{self.PATH}')
        self.model = None
        self.lose_list = None
        clear_log_debug()
        #

    def load(self, file_name):
        self.model = load_model(file_name)
        log_debug("model loaded: " +str(file_name))

    def save(self, file_name):
        self.model.save(file_name)
        log_debug("model saved: " +str(file_name))

    def train_ch6(self, dic):
        print("90155-cyber_ch6: \n", "="*50, "\n", dic, "\n", "="*50)


        result = {"status": "ok ch6"}
        return result

    def get_session(self, dic):
        print("90600-cyber get_session: \n", "="*50, "\n", dic, "\n", "="*50)
        u = "https://www.simplilearn.com/tutorials/"
        c = dic["course"]
        value = dic["value"]

        if value == "brute-force-attack":
            c = "cryptography-tutorial"

        u += c+"/"+value
        print(u)
        is_list = 0
        try:
            is_list = int(dic["is_list"])
        except Exception as ex:
            pass
        is_article = 0
        try:
            is_article = int(dic["is_article"])
        except Exception as ex:
            pass

        headers = {'User-Agent': 'amos@drbaranes.com'}
        resp = requests.get(u, headers=headers)

        # Force the correct encoding
        resp.encoding = 'utf-8'  # Ensure the response is decoded as UTF-8
        soup = BeautifulSoup(resp.text, 'html.parser')


        dl = {}
        dl[0] = ""
        dl[1] = "https://youtu.be/z5nc9MDbvkw?t=40"
        dl[2] = "https://youtu.be/wMRzjwYMou0"
        dl[3] = "https://youtu.be/cwQlRIpaLLo"
        dl[4] = "https://youtu.be/gK73JLEbDs0"
        dl[5] = "https://youtu.be/RWSqDF_6n4k"
        dl[6] = "https://youtu.be/QzP-B69LC5o"
        dl[7] = "https://youtu.be/33dHULn140M"
        dl[8] = "https://youtu.be/9GZlVOafYTg"
        dl[9] = "https://youtu.be/r6GlzIWiMD0"
        dl[10] = "https://youtu.be/nduoUEHrK_4"
        dl[11] = "https://youtu.be/-KL9APUjj3E"
        dl[12] = "https://youtu.be/Lc2Uv4_-GZ0"
        dl[13] = "https://youtu.be/ak9fzojnMaM"
        dl[14] = "https://youtu.be/mmuNuFBm-Ek"
        dl[15] = "https://youtu.be/y6E_CxkLLw8"
        dl[16] = "https://youtu.be/fUeJtM1bgGo"
        dl[17] = "https://youtu.be/nLKtI99f0es"
        dl[18] = "https://youtu.be/q5pQ_YtJWpA"
        dl[19] = "https://youtu.be/XkaJ3IPqGLw"
        dl[20] = "https://youtu.be/U3LMnJSNsLY"
        dl[21] = "https://youtu.be/vIOjzQPbMr4"
        dl[22] = "https://youtu.be/NoivU2LrUrI"
        dl[23] = ""
        dl[24] = ""
        dl[25] = ""
        dl[26] = ""
        dl[27] = ""
        dl[28] = ""
        dl[29] = ""
        dl[30] = ""
        dl[31] = ""
        dl[32] = ""
        dl[33] = ""
        dl[34] = ""
        dl[35] = ""
        dl[36] = ""
        dl[37] = ""
        dl[38] = ""
        dl[39] = ""
        dl[40] = ""
        dl[41] = "https://youtu.be/QGykYWbdf0A"
        dl[42] = "https://youtu.be/43yYsui3xZc"
        dl[43] = ""
        dl[44] = ""
        dl[45] = ""
        dl[46] = ""
        dl[47] = ""
        dl[48] = ""
        dl[49] = ""
        dl[50] = "https://youtu.be/IVpwBHLA-Wg"
        dl[51] = ""
        dl[52] = ""
        dl[53] = ""
        dl[54] = ""
        dl[55] = ""
        dl[56] = ""
        dl[57] = ""
        dl[58] = "https://youtu.be/FDuW2NDq5GU"
        dl[59] = "https://youtu.be/vf1WS15JiCo"
        dl[60] = "https://youtu.be/WiI9cCgaHcs"
        dl[61] = "https://youtu.be/Ig8t6MhroB8"
        dl[62] = "https://youtu.be/dUX8A6VTqdk"
        dl[63] = "https://youtu.be/1lzIgFci4zM"
        dl[64] = "https://youtu.be/HNefQ1J4eFk"

        l = [(0,"","Overview","")]
        if is_list == 1:
            topics = soup.find(class_="content-scrollable")
            tags = topics.find_all("a")
            for tag in tags:
                # pprint.pprint(tag)
                h = tag.get('href').split("/")[-1]
                t = tag.find("h4").text
                s = tag.find("span").text.split("-")[-1].strip()
                v = ''
                try:
                    v = dl[int(s)]
                except Exception as ex:
                    pass
                l.append((s,h,t,v))

            # pprint.pprint(l)

        tt = ""
        if is_article == 1:
            if value == "":
                tt = soup.find(id='videoPage')
            else:
                tt = soup.find('article')
            try:
                tags = tt.find_all(class_="detail-info-banner")
                for tag in tags:
                    tag.decompose()
                k = tt.find(id="Imageload")
                if k:
                    k.decompose()

                k = tt.find(id="aboutAuthor")
                if k:
                    k.decompose()
            except Exception as ex:
                print("Error 1115-11", ex)

            if value == "":
                k = tt.find(class_="video-inform")
                if k:
                    k.decompose()
                k = tt.find(id="recommendedCourses")
                if k:
                    k.decompose()
                k = tt.find(id="suggestedResources")
                if k:
                    k.decompose()
                k = tt.find(id="lvclink")
                if k:
                    k.decompose()
                if k:
                    k.decompose()
                k = tt.find(class_="article-info test-class")
                if k:
                    k.decompose()
                k = tt.find(class_="jumpLinks")
                if k:
                    k.decompose()
                k = tt.find(id="SkillCoveredViewMore")
                if k:
                    k.decompose()
                k = tt.find(class_="sticky-btn-info")
                if k:
                    k.decompose()
            else:
                try:
                    k = tt.find(id="suggestedResources")
                    if k:
                        k.decompose()

                    ks = tt.find_all(class_="info-details")
                    for k in ks:
                        k.decompose()

                    tags = tt.find_all(class_="btn")
                    for tag in tags:
                        tag.decompose()

                    tags = tt.find_all(id="how_can_simplilearn_help_you")
                    for tag in tags:
                        # tag.parent.decompose()
                        tag.decompose()

                    tags = tt.find_all("p")
                    for tag in tags:
                        text = tag.get_text()
                        if "Simplilearn" in text or "Expert Master’s Program" in text or "feel free " in text:
                            tag.decompose()

                except Exception as ex:
                    print("Error 3625", ex)

                try:
                    tags = tt.find_all("blockquote")
                    for tag in tags:
                        # print(tag)
                        text = tag.get_text()
                        if ("Enroll" in text or "career" in text or "Bootcamp" in text or
                                "Cyber security course" in text or
                                "Cybersecurity professionals can make between" in text or
                                "Certified Ethical Hacking Course" in text or
                                "Advanced Executive Program in Cybersecurity" in text):
                            # print(text)
                            tag.decompose()
                except Exception as ex:
                    print("Error 100-9010")
                try:
                    tags = tt.find_all("p")
                    for tag in tags:
                        # print(tag)
                        text = tag.get_text()
                        if "Bootcamp" in text:
                            # print(text)
                            tag.decompose()
                except Exception as ex:
                    print("Error 100-100")
                # print("A1001", tt)


            try:
                tags = tt.find_all("a")
                for a_tag in tags:
                    try:
                        # print(a_tag)
                        ref = a_tag.get('href').split("/")
                        u = ref[-2]
                        link = ref[-1]
                        # print(u, link)
                        span_tag = soup.new_tag('span')
                        try:
                            span_tag.string = a_tag.string  # Preserve the text content of the <a> tag
                        except Exception as ex:
                            pass
                        span_tag['class'] = a_tag.get('class', [])  # Preserve the class attribute

                        if u == "cyber-security-tutorial":
                            span_tag['style'] = "text-decoration: underline; cursor: pointer; color: blue;"
                            span_tag['onclick'] = "call_fun_for_obj(e=getEBI(9),fun='change',param='param',select_value='"+link+"')"
                        else:
                            span_tag['style'] = "text-decoration: underline;"

                        try:
                            a_tag.replace_with(span_tag)
                        except Exception as ex:
                            print("Error 110--11", ex)
                    except Exception as ex:
                        print(a_tag, "\nu=", u)
                        print("Error 22-22", ex)
            except Exception as ex:
                print("Error 444-222", ex)

            try:
                imgs = tt.find_all("img")
                for img in imgs:
                    # pprint.pprint(img)
                    img["src"] = img["data-src"]
            except Exception as ex:
                pass
            #
            tt = str(tt) + "<br><br><br><div>The End</div>"
            # print(tt.prettify())

        result = {"status": "ok", "l":l, "article": tt}
        return result

# CH 7
#