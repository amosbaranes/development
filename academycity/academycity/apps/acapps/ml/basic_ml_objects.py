import warnings
import os
from django.conf import settings
import matplotlib as mpl
import numpy as np
import pandas as pd
from django.apps import apps
from openpyxl import Workbook, load_workbook
import math
#
from ...core.utils import Debug
#
import matplotlib.pyplot as plt
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


class BaseDataProcessing(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90001-03 BaseDataProcessing", dic, '\n', '-'*50)
        super(BaseDataProcessing, self).__init__(dic)
        # print("90001-04 BaseDataProcessing", dic, '\n', '-'*50)
        self.name = 'DataProcessing'
        self.uploaded_filename = None
        # print("90003-0 PBaseDataProcessing", dic, '-'*50)

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
        self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", dic["app"])
        # print(self.PROJECT_ROOT_DIR)
        # print('-'*50)
        os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)
        self.TOPIC_ID = dic["topic_id"]  # "fundamentals"
        self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
        os.makedirs(self.TO_DATA_PATH, exist_ok=True)
        self.TO_EXCEL = os.path.join(self.TO_DATA_PATH, "excel", self.TOPIC_ID)
        os.makedirs(self.TO_EXCEL, exist_ok=True)
        self.TO_EXCEL_OUTPUT = os.path.join(self.TO_EXCEL, "output")
        os.makedirs(self.TO_EXCEL_OUTPUT, exist_ok=True)
        self.IMAGES_PATH = os.path.join(self.PROJECT_ROOT_DIR, "images")
        os.makedirs(self.IMAGES_PATH, exist_ok=True)
        self.MODELS_PATH = os.path.join(self.PROJECT_ROOT_DIR, "models")
        os.makedirs(self.MODELS_PATH, exist_ok=True)
        self.target_folder = None

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
        print("9002 BaseDataProcessing upload_file:")
        print(dic)
        # print("upload_file:")

        upload_file_ = dic["request"].FILES['drive_file']
        result = {}
        # We can extend and add another property: data_folder
        # like topic_id. But, we need to add this property to: params in the core view
        # and use it here.
        # for example: if data_folder=excel we choose self.TO_EXCEL

        # print("target_folder = self.TO_"+dic["folder_type"].upper())
        self.target_folder = eval("self.TO_" + dic["folder_type"].upper())

        filename = dic["request"].POST['filename']

        print(filename)

        self.uploaded_filename = filename
        file_path = os.path.join(self.target_folder, filename)
        with open(file_path, 'wb+') as destination:
            for c in upload_file_.chunks():
                destination.write(c)

        # print("9888-8 Uploaded\n", "-" * 30)
        result['file_path'] = file_path
        return result

    def get_general_data(self, dic):
        # print("9012 BaseDataProcessing get_general_data:\n", dic)
        app_ = dic["app"]

        # dic = {"app": "avi",
        #        "dimensions": {"time_dim": {"model": "TimeDim", "field_name": "year"},
        #                       "country_dim": {"model": "CountryDim", "field_name": "country_name"} }}

        result = {}
        n__=0
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

    def clean_name(self, name):
        name_ = name.replace("-", "").replace(" ", "").replace("_", "")
        return name_


class BasePotentialAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90050-01 BasePotentialAlgo", dic, '\n', '-'*50)
        super(BasePotentialAlgo, self).__init__()
        # print("90050-02 PotentialAlgo", dic, '\n', '-'*50)
        self.second_time_save = ''
        self.to_save = []
        self.to_save_all = []
        self.save_to_file = None
        self.df_index = None
        app_ = dic["app"]
        country_model_name_ = dic["country_model"]
        measure_model_name_ = dic["measure_model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=country_model_name_)
        model_measure_dim = apps.get_model(app_label=app_, model_name=measure_model_name_)
        # print(model_measure_dim)
        self.countries_name = pd.DataFrame(model_country_dim.objects.all().values('id', 'country_name'))
        self.measures_name = pd.DataFrame(model_measure_dim.objects.all().values('id', 'measure_name'))
        # print(self.measures_name)
        self.options = ["mm", "mx", "xm", "xx"]
        self.is_calculate_min_max = None

    def process_algo(self, dic):
        # print("9015 BasePotentialAlgo process_algo\n", dic)
        app_ = dic["app"]
        fact_model_name_ = dic["fact_model"]
        min_max_model_name_ = dic["min_max_model"]
        measure_group_model_name_ = dic["measure_group_model"]
        model_fact = apps.get_model(app_label=app_, model_name=fact_model_name_)
        try:
            self.is_calculate_min_max = eval(dic["is_calculate_min_max"])
            # print(self.is_calculate_min_max)
        except Exception as ex:
            print("Error 9016: \n"+str(ex))
        if not self.is_calculate_min_max:
            model_min_max = apps.get_model(app_label=app_, model_name=min_max_model_name_)
        model_measure_group = apps.get_model(app_label=app_, model_name=measure_group_model_name_)

        # print("90060-10 PotentialAlgo: \n", dic, "\n", "="*50)
        wb2 = None
        groups = model_measure_group.objects.all()
        nn__ = 0
        sign_n1 = pd.DataFrame([[0, 0, 0, 0]])
        sign_n2 = pd.DataFrame([[0, 0, 0, 0]])
        sign_n1.columns = self.options
        sign_n2.columns = self.options
        similarity_n1 = pd.DataFrame([[0, 0, 0, 0]])
        similarity_n2 = pd.DataFrame([[0, 0, 0, 0]])
        contribution_n1 = pd.DataFrame([[0, 0, 0, 0]])
        contribution_n2 = pd.DataFrame([[0, 0, 0, 0]])
        # relimp_n1 = pd.DataFrame([[0, 0, 0, 0]])
        # relimp_n2 = pd.DataFrame([[0, 0, 0, 0]])
        similarity_n1.columns = self.options
        similarity_n2.columns = self.options
        group_d = ""
        for k in groups:
            group = k.group_name
            # print("="*50)
            # print(group)
            # print("="*50)
            try:
                self.save_to_file = os.path.join(self.TO_EXCEL_OUTPUT, str(dic["time_dim_value"]) + "_" + group + "_o.xlsx")
                self.to_save = []
                # print("file_path\n", self.save_to_file, "\n", "="*50)
                s = ""
                for v in dic["axes"]:
                    s += "'" + v + "',"
                s += "'" + dic["value"] + "'"
                # print(dic["time_dim_value"])
                qs = model_fact.objects.filter(measure_dim__measure_group_dim__group_name=group,
                                               time_dim_id=dic["time_dim_value"]).all()
                s = "pd.DataFrame(list(qs.values(" + s + ")))"
                df = eval(s)
                if df.shape[0] == 0:
                    continue
                # print("50001-21")
                df = df.pivot(index="country_dim", columns='measure_dim', values='amount')
                # print(df)
                # print("50001-22")
                self.df_index = df.index
                df_columns = df.columns
                # print(df)
                # print("50001-22-1")
                df_ = self.add_country_to_df(df)
                self.to_save.append((df_.copy(), 'Data'))
                #
                if not self.is_calculate_min_max:
                    qs_mm = model_min_max.objects.filter(measure_dim__measure_group_dim__group_name=group,
                                                         time_dim_id=dic["time_dim_value"]).all()
                    df_mm = pd.DataFrame(list(qs_mm.values('measure_dim', 'min', 'max')))
                    first_row = pd.DataFrame(df_mm.T.loc["min"]).T.reset_index().drop(['index'], axis=1)
                    # print(first_row)
                    second_row = pd.DataFrame(df_mm.T.loc["max"]).T.reset_index().drop(['index'], axis=1)
                    # print(second_row)
                else:
                    df = df.apply(pd.to_numeric, errors='coerce').round(6)
                    df_q=df.quantile([0.25, 0.5, 0.75])
                    diff_qm25 = df_q.iloc[1].subtract(df_q.iloc[0], fill_value=None)*1.5
                    diff_qm75 = df_q.iloc[2].subtract(df_q.iloc[1], fill_value=None)*1.5
                    first_row = pd.DataFrame(df_q.iloc[0] - diff_qm25).T
                    second_row = pd.DataFrame(df_q.iloc[1] + diff_qm75).T
                first_row.columns = df_columns
                second_row.columns = df_columns
                diff_row = second_row.subtract(first_row, fill_value=None)
                diff_row.columns = df_columns
                # print(first_row)
                # print(second_row)
                # print("4000-2")
                # print("6 df_columns\n", df_columns, "\ndiff_row\n", diff_row, "\n", "="*100)
                df_n1 = df.copy()
                try:
                    df_n1 = df_n1.astype(float)
                except Exception as ex:
                    print("1000: " + str(ex))
                for i, r in df_n1.iterrows():
                    for j in df_columns:
                        try:
                            z = (r[j] - first_row[j].astype(float)) / diff_row[j].astype(float)
                            df_n1.loc[i][j] = z
                        except Exception as ex:
                            print("Error i " + str(i) + " " + str(ex))
                # print("1 df_n1\n", df_n1, "\n", "="*100)
                df_n1 = df_n1.apply(pd.to_numeric, errors='coerce').round(6)
                self.add_to_save(title='Normalized-1', a=df_n1, cols=None)
                #
                # print("50001-2")
                df_n2 = df_n1.copy()
                df_n2[df_n2 < 0] = 0
                df_n2[df_n2 > 1] = 1
                self.add_to_save(title='Normalized-2', a=df_n2, cols=None)
                #
                # print(group)
                if len(df_n1.columns) < 2:
                    df_n1["max"] = df_n1[df_n1.columns[0]]  # df_n1["Birth Rate"]
                    df_n2["max"] = df_n2[df_n2.columns[0]]  # df_n2["Birth Rate"]
                    df_1_2 = pd.merge(left=df_n1, right=df_n2, left_index=True, right_index=True)
                    # df_1_2.columns = ['min-n1', 'max-n1', 'min-n2', 'max-n2']
                    # cols = df_1_2.columns
                    # cols = cols.insert(0, 'country_name')
                    # self.add_to_save(title='min-max', a=df_1_2, cols=cols)
                elif len(df_n1.columns) < 5:
                    # print("-1"*30)
                    # print(group)
                    # print("-000"*30)
                    df_n1 = df_n1.apply(lambda x: np.sort(x), axis=1, raw=True)
                    df_n2 = df_n2.apply(lambda x: np.sort(x), axis=1, raw=True)
                    df_n1["max"] = df_n1.max(axis=1)
                    df_n1["min"] = df_n1.min(axis=1)
                    df_n2["max"] = df_n2.max(axis=1)
                    df_n2["min"] = df_n2.min(axis=1)
                    # df_n1 = df_n1.drop(df_n1_columns, axis=1)
                    # df_n2 = df_n2.drop(df_n2_columns, axis=1)
                    df_n1 = df_n1[["min", "max"]]
                    df_n2 = df_n2[["min", "max"]]
                    df_1_2 = pd.merge(left=df_n1, right=df_n2, left_index=True, right_index=True)
                    # df_1_2.columns = ['min-n1', 'max-n1', 'min-n2', 'max-n2']
                    # cols = df_1_2.columns
                    # cols = cols.insert(0, 'country_name')
                    # df_ = self.add_country_to_df(df_1_2, cols)
                    # print(df_)
                    # self.to_save.append((df_.copy(), 'min-max'))
                else:
                    zero_list = {}
                    one_list = {}
                    # print(df_n1)
                    for i in df_n1.index:
                        n0 = []
                        n1 = []
                        for num in df_n1.loc[i]:
                            if not pd.isna(num):
                                if num <= 0:
                                    n0.append(num)
                                elif num >= 1:
                                    n1.append(num)
                        if len(n0) > 0:
                            # print("n0\n", n0)
                            n0.sort(reverse=True)
                            # print("A n0\n", n0)
                            # print("="*10)
                            zero_list[i] = n0
                        elif len(n1) > 0:
                            n1.sort()
                            one_list[i] = n1
                    # # #
                    a = df_n2.values
                    a_1 = a.copy()
                    a_1.sort(axis=1)
                    self.add_to_save(title='Sort L', a=a_1, cols=-1)
                    a_1 = self.clean_rows(a=a_1, j=1, side="L")
                    #
                    a_1m = pd.DataFrame(a_1)
                    a_1m = a_1m.apply(self.move_elements_to_right, axis=1)
                    a_1m = a_1m.apply(self.revers_elements_in_row, axis=1)
                    self.add_to_save(title='R arranged', a=a_1m, cols=-1)
                    #
                    a_1 = -1 * a_1.copy()
                    a_1.sort(axis=1)
                    self.add_to_save(title='Sort R', a=a_1, cols=-1)
                    a_1 = self.clean_rows(a=a_1, j=1, side="R")
                    a_1 = -1 * a_1.copy()
                    a_1.sort(axis=1)
                    #
                    # move the numbers to the right.
                    # a_1 = pd.DataFrame(a_1)
                    # a_1 = a_1.apply(self.revers_elements_in_row, axis=1)
                    # print(a_1)
                    #
                    self.add_to_save(title='Final R', a=a_1, cols=-1)
                    # print(a_1)
                    # a_1 = -1 * a_1
                    # a_1 = a_1.apply(self.revers_elements_in_row, axis=1)
                    # a_1.sort(axis=1)  #
                    # self.add_to_save(title='Final-1', a=a_1, cols=-1)
                    # # #
                    a_1 = pd.DataFrame(a_1)
                    a_1.dropna(how='all', axis=1, inplace=True)
                    # print("600000000-100-1")
                    #
                    a_1 = a_1.apply(self.twenty_rule, axis=1)
                    # print("600000000-100-12")
                    a_1 = a_1.apply(lambda x: np.sort(x), axis=1, raw=True)
                    # print("600000000-100-13")
                    self.add_to_save(title='Final-20-rule', a=a_1, cols=-1)

                    # print("600000000-100-2")

                    a_1 = a_1.apply(self.twentyfive_rule, axis=1)
                    self.add_to_save(title='Final-25-rule', a=a_1, cols=-1)
                    a_2 = a_1.copy()
                    #
                    # print("zero_list\n", zero_list)
                    ff = []
                    for j in a_1.index:
                        nn = list(a_1.loc[j])
                        # print("nn == \n", nn)
                        if min(nn) == 0:
                            # print("nn zero_list[j]\n", zero_list[j])
                            nn = [zero_list[j].pop(0) if i == 0 else i for i in nn]
                            # print("nn 0\n", nn)
                        if max(nn) == 1:
                            nn = [one_list[j].pop() if i == 1 else i for i in nn]
                            # print("nn 1\n", nn)
                        # nn.insert(0, j)
                        nn.sort()
                        ff.append(nn)
                    self.add_to_save(title='Final-25-rule-n1', a=ff, cols=-1)
                    a_1 = pd.DataFrame(ff, index=list(self.df_index))
                    #
                    df_n1 = a_1.apply(self.min_max_rule, axis=1)
                    df_n1.columns = ['min-n1', 'max-n1']
                    #
                    df_n2 = a_2.apply(self.min_max_rule, axis=1)
                    df_n2.columns = ['min-n2', 'max-n2']
                    df_1_2 = pd.merge(left=df_n1, right=df_n2, left_index=True, right_index=True)

                # print("50001-3")

                df_1_2.columns = ['min-n1', 'max-n1', 'min-n2', 'max-n2']
                cols = df_1_2.columns
                cols = cols.insert(0, 'country_name')
                # print("50001-3-6")
                self.add_to_save(title='min-max', a=df_1_2, cols=cols)
                # self.add_to_save(title='min-max', a=df_1_2, cols=-1)
                # print("50001-3-9")
                self.save_to_excel_()

                # print("50001-3-9-1")
            except Exception as ex:
                print("Error 50001-1: " + str(ex))
            df_n1_ = df_n1.copy()
            df_n1_.columns = ['m-' + group, 'x-' + group]
            df_n2_ = df_n2.copy()
            df_n2_.columns = ['m-' + group, 'x-' + group]
            if nn__ == 0:
                ss_n_mm = ""
                ss_n_xm = ""
                ss_n_mx = ""
                ss_n_xx = ""
                group_d = group
                df_n1_all = df_n1_
                df_n2_all = df_n2_
                nn__ += 1
            else:
                # print(group_d, group)
                group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2, similarity_n1, similarity_n2 = \
                    self.create_similarity(group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2,
                                           similarity_n1, similarity_n2)
                ss_n_mm += '"' + group_d + '-' + group + '-mm",'
                ss_n_mx += '"' + group_d + '-' + group + '-mx",'
                ss_n_xm += '"' + group_d + '-' + group + '-xm",'
                ss_n_xx += '"' + group_d + '-' + group + '-xx",'

        ss_n_mm = ss_n_mm[:-1]
        ss_n_mx = ss_n_mx[:-1]
        ss_n_xm = ss_n_xm[:-1]
        ss_n_xx = ss_n_xx[:-1]

        for n in ["1", "2"]:
            ll = []
            for k in self.options:
                exec("df_n" + n + "_all['d_" + k + "']=df_n" + n + "_all[[" + eval("ss_n_" + k) + "]].min(axis=1)")
                exec("ll.append(1-df_n" + n + "_all[[" + eval("ss_n_" + k) + "]].min(axis=1).mean())")
            exec("similarity_n" + n + ".loc['SComb'] = ll")
            exec("sign_n" + n + ".drop([0], axis=0, inplace=True)")
            self.add_to_save_all(title='sign-n' + n, a=eval("sign_n" + n), cols=-1)
            exec("similarity_n" + n + ".drop([0], axis=0, inplace=True)")
            self.add_to_save_all(title='similarity-n' + n, a=eval("similarity_n" + n), cols=-1)
        for n in ["1", "2"]:
            nn__ = 0
            llg = []
            for k in groups:
                group = k.group_name
                print("-"*10)
                print(group)
                if nn__ > 0:
                    ll = []
                    for z in self.options:
                        s_ = "df_n" + n + "_all['dc_" + group + "_" + z + "'] = abs("
                        s_ += "df_n" + n + "_all['d_" + z + "'] - "
                        s_ += "df_n" + n + "_all['" + group_d + "-" + group + "-" + z + "'])"
                        exec(s_)
                        # print('ll.append(1-df_n'+n+'_all["dc_'+group+'_' + z+'"].mean())')
                        exec('ll.append(1-df_n' + n + '_all["dc_' + group + '_' + z + '"].mean())')

                    llc = [x - 0.7 for x in ll]
                    llg.append(llc)
                    llc = llc / sum(llc)
                    exec("contribution_n" + n + ".loc[group] = ll")
                else:
                    nn__ += 1

            self.add_to_save_all(title="all-n" + n, a=eval("df_n" + n + "_all"), cols=-1)
            exec("contribution_n" + n + ".columns = self.options")
            exec("contribution_n" + n + ".drop([0], axis=0, inplace=True)")
            # print("="*50)
            npg = np.array(llg)
            npgs = np.sum(llg, axis=0)
            df_relimp = pd.DataFrame(npg/npgs, index=contribution_n1.index)
            df_relimp.columns = self.options
            # print(df_relimp)
            self.add_to_save_all(title='contribution-n' + n, a=eval("contribution_n" + n), cols=-1)
            self.add_to_save_all(title='relimp-n' + n, a=df_relimp, cols=-1)
        # for n in ["1", "2"]:
        #     nn__ = 0
        #     for k in groups:
        #         group = k.group_name
        #         print("-"*10)
        #         print(group)
        #         if nn__ > 0:
        #             ll = []
        #             for z in self.options:
        #                 s_ = "df_n" + n + "_all['dc_" + group + "_" + z + "'] = abs("
        #                 s_ += "df_n" + n + "_all['d_" + z + "'] - "
        #                 s_ += "df_n" + n + "_all['" + group_d + "-" + group + "-" + z + "'])"
        #                 exec(s_)
        #                 # print('ll.append(1-df_n'+n+'_all["dc_'+group+'_' + z+'"].mean())')
        #                 exec('ll.append(1-df_n' + n + '_all["dc_' + group + '_' + z + '"].mean())')
        #             llc = [x - 0.7 for x in ll]
        #             llc = llc / sum(llc)
        #             exec("contribution_n" + n + ".loc[group] = ll")
        #             exec("relimp_n" + n + ".loc[group] = llc")
        #         else:
        #             nn__ += 1
        #     self.add_to_save_all(title="all-n" + n, a=eval("df_n" + n + "_all"), cols=-1)
        #     exec("contribution_n" + n + ".columns = self.options")
        #     exec("relimp_n" + n + ".columns = self.options")
        #     exec("contribution_n" + n + ".drop([0], axis=0, inplace=True)")
        #     exec("relimp_n" + n + ".drop([0], axis=0, inplace=True)")
        #     # print(eval("contribution_n"+n))
        #     # print(eval("relimp_n"+n))
        #     self.add_to_save_all(title='contribution-n' + n, a=eval("contribution_n" + n), cols=-1)
        #     self.add_to_save_all(title='relimp-n' + n, a=eval("relimp_n" + n), cols=-1)
        self.save_to_excel_all_(dic["time_dim_value"])

        result = {"status": "ok"}
        return result

    def create_similarity(self, group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2,
                          similarity_n1, similarity_n2):
        df_n1_all = pd.merge(left=df_n1_all, how='outer', right=df_n1_, left_index=True, right_index=True)
        df_n2_all = pd.merge(left=df_n2_all, how='outer', right=df_n2_, left_index=True, right_index=True)
        # print(df_n2_all.head(100))
        for n in ["1", "2"]:
            # print(n)
            ll = []
            lls = []
            for k in self.options:
                # print(k[0], k[1])
                # print("abs(df_n"+n+"_all['"+k[0]+"-" + group_d + "'] - df_n"+n+"_all['"+k[1]+"-" + group + "'])")
                df_d = eval("abs(df_n" + n + "_all['" + k[0] + "-" + group_d + "'] - df_n" + n + "_all['" + k[
                    1] + "-" + group + "'])")
                # print(df_d.head())
                s_d = df_d.sum()
                # print(s_d)
                df_r = eval("abs(df_n" + n + "_all['" + k[0] + "-" + group_d + "'] - 1 + df_n" + n + "_all['" + k[
                    1] + "-" + group + "'])")
                s_r = df_r.sum()
                # print(s_r)
                if s_d < s_r:
                    d_ = s_d
                    exec("df_n" + n + "_all['" + group_d + '-' + group + '-' + k + "'] = df_d")
                    lls.append(1 - df_d.mean())
                    ll.append(1)
                else:
                    d_ = s_r
                    exec("df_n" + n + "_all['" + group_d + '-' + group + '-' + k + "'] = df_r")
                    lls.append(1 - df_r.mean())
                    ll.append(-1)
            exec("sign_n" + n + ".loc[group] = ll")
            exec("similarity_n" + n + ".loc[group] = lls")

        return group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2, similarity_n1, similarity_n2

    def add_country_to_df(self, df, cols=None):
        df_ = df.copy()
        if cols is None:
            # print("BB2")
            cols = ['country_name']
            df_c = df.columns
            for j in df_c:
                k = str(self.measures_name[self.measures_name["id"] == j]["measure_name"]).split("    ")[1].split("\n")[
                    0]
                cols.append(k)
        # print("add_country_to_df", 1)
        df_ = df_.reset_index()
        # print("-"*10, "\nAA\n", "\n", df_)
        df_ = df_.merge(self.countries_name, how='inner', left_on='country_dim', right_on='id').drop(
            ['country_dim', 'id'], axis=1)
        # print("BB3\n", "\n", df_)
        c_ = df_.pop('country_name')
        df_.insert(0, 'country_name', c_)
        # print("CC\n", "\n", df_)
        # print("CC1\n", df_.columns, "\n", cols)
        if isinstance(cols, pd.core.indexes.base.Index) or cols != -1:
            df_.columns = cols
        # print("DD\n", "\n", df_)
        return df_

    # It seems that I can delete this function
    def save_to_excel(self, df, folder):
        df2 = df.copy()
        # print(self.save_to_file + ' -Before sleep save_to_excel- ' + folder)
        total, used, free = shutil.disk_usage("/")
        # print(' total: ' + str(total) + ' used: ' + str(used) + ' free: ' + str(free))
        nnn = 0
        try:
            with pd.ExcelWriter(self.save_to_file, engine='openpyxl', mode='a') as writer_:
                df2.to_excel(writer_, sheet_name=folder)
                writer_.save()
                time.sleep(5)
            if self.second_time_save != '':
                print("save ok:", self.second_time_save)
            self.second_time_save = ''
            nnn = 1
        except Exception as ee:
            print(ee)
            time.sleep(5)
            self.save_to_excel(df2, folder)
            self.second_time_save = self.save_to_file
            nnn = 1
        finally:
            if nnn == 0:
                print(self.save_to_file + ' 55 finally -' + str(nnn) + ' - ' + folder)
                time.sleep(5)
                print(self.save_to_file + ' 551 finally -' + str(nnn) + ' - ' + folder)
                self.save_to_excel(df2, folder)
                self.second_time_save = self.save_to_file

    def save_to_excel_(self):
        wb2 = Workbook()
        wb2.save(self.save_to_file)
        wb2.close()
        wb2 = None
        # print("save_to_excel_", self.save_to_file)

        with pd.ExcelWriter(self.save_to_file, engine='openpyxl', mode="a") as writer_o:
            for d in self.to_save:
                try:
                    # print("d[0]\n", d[0])
                    # print("d[1]\n", d[1])
                    d[0].to_excel(writer_o, sheet_name=d[1])
                except Exception as ex:
                    print("9006-3 " + str(ex))
            writer_o.save()
        wb = load_workbook(filename=self.save_to_file, read_only=False)
        del wb['Sheet']
        wb.save(self.save_to_file)
        wb.close()

    def save_to_excel_all_(self, year):
        save_to_file_all = os.path.join(self.TO_EXCEL_OUTPUT, "all_" + str(year) + ".xlsx")
        # print("save_to_excel_all_", save_to_file_all)
        wb2 = Workbook()
        wb2.save(save_to_file_all)
        wb2.close()

        with pd.ExcelWriter(save_to_file_all, engine='openpyxl', mode="a") as writer:
            for d in self.to_save_all:
                try:
                    d[0].to_excel(writer, sheet_name=d[1])
                except Exception as ex:
                    print("9006-3 " + d[2] + str(ex))
            writer.save()

        # wb = load_workbook(filename=save_to_file_all, read_only=False)
        # del wb['Sheet']
        # wb.save(self.save_to_file)
        # wb.close()

    def add_to_save(self, title, a, cols):
        ai = pd.DataFrame(a)
        ai.index = self.df_index
        df_ = self.add_country_to_df(ai, cols=cols)
        df_.dropna(how='all', axis=1, inplace=True)
        self.to_save.append((df_.copy(), title))

    def add_to_save_all(self, title, a, cols):
        ai = pd.DataFrame(a)
        ai.dropna(how='all', axis=1, inplace=True)
        self.to_save_all.append((ai.copy(), title))

    def clean_rows(self, a, j, side="L"):
        # print("j", j)
        # a.sort(axis=1)
        # if j == 1:
        # self.add_to_save(title='Sort '+side+"-"+str(j), a=a, cols=-1)
        #
        a_ = pd.DataFrame(a.copy())
        a_ = a_.loc[a_.apply(lambda x: x.count(), axis=1) > 4]
        a_ = a_.to_numpy()
        # print(a.shape, "\n", a_.shape)
        if a_.shape[0] == 0:
            return a
        d = a[:, j:1 + j] - a[:, 0:1]
        d_ = a_[:, j:1 + j] - a_[:, 0:1]
        d_m = np.nanmean(d_, axis=0)
        # print(j, "\n", d_m, "\n", d_m[0])
        if d_m[0] < 0.03:
            #
            df_d = pd.DataFrame(d)
            df_d.index = self.df_index
            df_ = self.add_country_to_df(df_d, cols=-1)
            self.to_save.append((df_.copy(), 'D_' + side + ' - ' + str(j)))
            # print("d=\n", d)
            #
            b = pd.DataFrame(a.copy())
            b.loc[b.apply(lambda x: x.count(), axis=1) > 4, [j]] = np.nan
            #
            b.index = self.df_index
            df_ = self.add_country_to_df(b, cols=-1)
            self.to_save.append((df_.copy(), side + ' b ' + str(j)))
            #
            b = b.to_numpy()
            if j + 1 < b.shape[1]:
                b = self.clean_rows(b, j + 1, side)
        else:
            b = a.copy()
        return b

    def move_elements_to_right(self, row):
        n_nna = row.count()
        n_na = row.isna().sum().sum()
        n = n_na + n_nna
        # print("line 1 row=", n, n_na, n_nna)
        # print(row)
        row_c = row.copy()
        for j in range(n-1):
            try:
                if str(row_c[n-j-1:n-j].iloc[0]) == "nan":
                    for z in range(0, n-1-j):
                        if str(row_c[n-j-2-z:n-j-1-z].iloc[0]) != "nan":
                            row_c[n-j-1:n-j].iloc[0] = row_c[n-j-2-z:n-j-1-z].iloc[0]
                            row_c[n-j-2-z:n-j-1-z].iloc[0] = np.nan
                            break
            except Exception as ex:
                print("ex1: "+str(ex))
        # print("-"*100)
        # print(row)
        # print(row_c)
        # print("-"*100)
        return row_c

    def revers_elements_in_row(self, row):
        n_nna = row.count()
        n_na = row.isna().sum().sum()
        n = n_na + n_nna
        row_ = row.copy()
        for j in range(n):
            row_[j:j+1] = row[n-j-1:n-j]
        return row_

    def twenty_rule(self, row):
        # print("-1"*10, "\nrow:\n", row, "-2"*10, "\n")
        n_row = row.count()
        # print("n_row= ", n_row)
        if n_row < 5:
            n = 0
        elif n_row == 5:
            n = 1
        else:
            n = math.ceil(n_row * 0.2)
        min = n_row
        row_best = row
        if n == 0:
            return row_best

        # print("-4"*10)
        # print("n= ", n, "\n range(n+1)=", range(n+1))
        # print("-5"*10)
        for j in range(n + 1):
            row_c = row.copy()
            row_c[:j] = np.nan
            # print("-6"*10)
            # print(row_c)
            # print("-7"*10)
            row_c[n_row - (n - j):] = np.nan
            # print(row_c)
            # print("-8"*10)
            # print("max=", row_c.max(), "min=", row_c.min())
            # print("-9"*10)
            if row_c.max() - row_c.min() < min:
                min = row_c.max() - row_c.min()
                row_best = row_c.copy()
        return row_best

    def twentyfive_rule(self, row):
        n_row = row.count()
        row_best = row
        if (n_row > 4) and (row.max() - row.min() > 0.25):
            n = 1
            min = n_row
            for j in range(n + 1):
                row_c = row.copy()
                row_c[:j] = np.nan
                row_c[n_row - (n - j):] = np.nan
                if (row_c.max() - row_c.min()) < min:
                    min = row_c.max() - row_c.min()
                    row_best = row_c.copy()
        if row_best.max() - row_best.min() > 0.25:
            row_best[:] = np.nan
        return row_best

    def min_max_rule(self, row):
        row_ = row[0:2].copy()
        row_[:] = np.nan
        row_[0] = row.min()
        row_[1] = row.max()
        return row_
