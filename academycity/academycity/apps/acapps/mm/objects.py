import warnings
import os
from django.conf import settings
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
import matplotlib as mpl
from django.apps import apps

import sys
import shutil
import pandas as pd
import numpy as np
import math
from openpyxl.utils.dataframe import dataframe_to_rows
import csv
import pickle
from concurrent.futures import ThreadPoolExecutor as T
from statistics import mean, median
import copy

from openpyxl import Workbook, load_workbook
from ...core.utils import log_debug, clear_log_debug

from collections import OrderedDict
from operator import getitem

mpl.use('Agg')


class MMAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90001-01 MSAlgo", dic, '\n', '-'*50)
        super(MMAlgo, self).__init__()
        # print("90001-02 MSAlgo", dic, '\n', '-'*50)

    def min_max_rule(self, row):
        row_ = row[0:2].copy()
        row_[:] = np.nan
        row_[0] = row.min()
        row_[1] = row.max()
        return row_

    def calculate_min_max_cuts(self, dic):
        print("90099-99-1000 MMAlgo calculate_min_max_cuts: \n", dic, "\n'", "="*50)

        app_ = dic["app"]
        method = dic["method"]
        #
        first_high_group = 0.4
        first_low_group = 0.4
        step = 0.05
        n_step = int(first_high_group/step)
        #

        u_method = "median"
        l_method = "median"
        if method == "min":
            u_method = "min"
            l_method = "max"

        model_fact = apps.get_model(app_label=app_, model_name="factnormalized")
        qs = model_fact.objects.all()
        df = pd.DataFrame(list(qs.values("gene_dim", "person_dim", "amount")))

        try:
            df = df.pivot(index="person_dim", columns='gene_dim', values='amount')
            # print("df1\n ", df)
            df = df.sort_values(df.columns[0], ascending=False)
            # print("df2\n ", df)
            df = df.reset_index()
        except Exception as ex:
            print(ex)

        print("'", "="*50)
        # print("90-111-2-100\n","\n", df,"\n")
        print(df.head(56),"\n", df.tail(56),"\n", df.shape)
        print("'", "="*50)
        step_num = int(df.shape[0]*step)
        print("step_num=", step_num)
        print("'", "="*30)

        # print(range(int(first_high_group*100), 0, -int(step*100)))

        def score(dic_hp):
            print(dic_hp)

        dic_hp = {}
        # int((first_low_group-step) * 100)
        for l in range(int(first_low_group * 100), int(step*100), -int(step * 100)):
            l_ = round(l - step*100)/100
            for h in range(int(first_high_group*100), int(step*100), -int(step*100)):
                h_ = (100 - round(h - step*100))/100
                print("\n", "-"*30, "\n  h=", h, "(h_=", h_, ") l=", l, " (l_=", l_,")\n","-"*30)
                ll = [h/100, (100-l)/100]
                # print("A ll=", ll)
                df_q = df.quantile(ll)
                print("-"*20)
                print("df_q\n", df_q[["person_dim"]])
                print("-"*20)
                # print(df_q[["person_dim"]].iloc[0], "\n\n", df_q[["person_dim"]].iloc[1])
                h_cut = (float(df_q[["person_dim"]].iloc[0])-1)*(df.shape[0]/(df.shape[0]+1))
                h_cut = int(round(h_cut))
                print(df.shape, "\nH cut index=", h_cut)
                print("-"*20)
                cond_h = df.index <= h_cut
                df_h_e = df[cond_h]
                print("Top records sorted by Y:\n", df_h_e.tail(56))
                # print(df_h_e.index)
                # print(len(df_h_e.index)-step_num-1)
                y_max_cut =df_h_e.iloc[len(df_h_e.index)-step_num-1][1]
                print("-"*30, "\nH", "person_index=", df_h_e.iloc[len(df_h_e.index)-step_num-1]["person_dim"],
                      "Y=", y_max_cut, "\n", "-"*30, "\n")

                l_cut = (float(df_q[["person_dim"]].iloc[1])-1)*(df.shape[0]/(df.shape[0]+1))
                l_cut = int(round(l_cut))
                cond_l = df.index > l_cut
                df_l_e = df[cond_l]

                print(df.shape, "\nL cut index=", l_cut)
                print("Low records sorted by Y:\n", df_l_e.head(56))
                # print(df_l_e.index)

                y_min_cut = df_l_e.iloc[step_num][1]
                print("-"*30, "\nL", "person_index=", df_l_e.iloc[step_num]["person_dim"],
                      "Y=", y_min_cut, "\n", "-"*30, "\n")

                # print(df_h_e.columns, len(df_h_e.columns))
                nhi_ = 0
                nli_ = 0

                for hi in range(h, int(step*100), -int(step*100)):
                    nhi_ += 1
                    hi_ = (100 - round(hi - step * 100)) / 100
                    for li in range(l, int(step*100), -int(step*100)):
                        nli_ += 1
                        li_ = round(li - step*100)/100
                        index_ = "h-"+str(h_) + "_" + "l-" + str(l_) + "_" + "hi-" + str(hi_) + "_" + "li-" + str(li_)
                        dic_hp[index_] = {}
                        dic_hp[index_]["y"] = {"max_cut": float(y_max_cut), "min_cut": float(y_min_cut)}
                        # print(dic_hp)
                        print(index_)

                        # for gene_num in range(len(df_h_e.columns)-1, 1, -1):
                        #     # l
                        #     print("li_", li_)
                        #     df_lx = df_l_e[[gene_num]].sort_values(gene_num, ascending=False)
                        #     # print(df_l_e[[gene_num]], "\n\n")
                        #     if nli_ == 1:
                        #         print("\nInternal Loop: variable(gene)=", gene_num, "li_=", li_, "sorted values:\n", df_lx, "\n")
                        #     lx = df_lx.iloc[len(df_lx.index) - nli_ * step_num - 1][gene_num]
                        #     li = pd.DataFrame(df_lx.iloc[len(df_lx.index) - nli_ * step_num - 1])
                        #     print(" Internal Loop: variable(gene)=", gene_num, "li_=", li_, "person index=",
                        #           li.columns[0], "value=", lx, "\n")
                        #     # h
                        #     print("hi_", hi_)
                        #     df_hx = df_h_e[[gene_num]].sort_values(gene_num, ascending=False)
                        #     # print(df_h_e[[gene_num]], "\n\n")
                        #     if nhi_ == 1:
                        #         print("\nInternal Loop: variable(gene)=", gene_num, "hi_=", hi_, "sorted values:\n", df_hx, "\n")
                        #     hx = df_hx.iloc[len(df_hx.index) - nhi_ * step_num - 1][gene_num]
                        #     hi = pd.DataFrame(df_hx.iloc[len(df_hx.index) - nhi_ * step_num - 1])
                        #     print(" Internal Loop: variable(gene)=", gene_num, "hi_=", hi_, "person index=",
                        #           hi.columns[0], "value=", hx, "\n")
                        #
                        #     dic_hp[index_][gene_num] = {"max_cut": float(hx), "min_cut": float(lx)}
                        #
                        #     print("="*30)
                        #     print(dic_hp)
                        #     print("="*30)

                print("'", "="*50)
                print("'", "="*50)
                print("'", "="*50)


        result = {"status": "ok"}
        return result



class MMDataProcessing(BaseDataProcessing, MMAlgo):
    def __init__(self, dic):
        super().__init__(dic)
        # print("90002-05 MMDataProcessing", dic, '\n', '-'*50)

    def load_file_to_db(self, dic):
        # print("90121-1: \n", dic, "="*50)
        # print(dic)
        # print('dic')
        clear_log_debug()
        log_debug("=== load_file_to_db 100 ===")
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # file_path = "/home/amos/projects/development/academycity/data/ms/datasets/excel/raw_data/RAW DATA (607).xlsx"
        # print('file_path')
        # print(file_path)
        # print('file_path')
        # print('90121-2 dic')

        dic = dic["cube_dic"]
        # print('90121-3 dic', dic)


        model_name_ = dic["dimensions"]["person_dim"]["model"]
        model_person_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["gene_dim"]["model"]
        model_gene_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        model_fact.truncate()
        model_gene_dim.truncate()
        model_person_dim.truncate()
        wb = load_workbook(filename=file_path, read_only=False)
        sheet_names = wb.sheetnames
        f = "Data"
        ws = wb[f]
        data = ws.values
        # Get the first line in file as a header line
        columns = next(data)[0:]
        # print(columns)
        # Create a DataFrame based on the second and subsequent lines of data
        df = pd.DataFrame(data, columns=columns)
        df = df.reset_index()  # make sure indexes pair with number of rows
        # n__ = 0

        list_ = []
        for index, row in df.iterrows():
            print("index", index)
            for j in range(1, len(columns)):
                # print("j", j)
                if row[1] is not None and str(row[1]) != "None" and str(row[1]) != "":
                    g_ = str(row[1])
                    # print("g_", g_)
                    gene_dim_obj, is_created = model_gene_dim.objects.get_or_create(gene_code=g_)
                    p_ = str(columns[j])
                    if p_ != "None" and p_ != "":
                        person_dim_obj, is_created = model_person_dim.objects.get_or_create(person_code=p_)
                    try:
                        # print(str(row[columns[j]]), "\n", "="*20)
                        v_ = float(str(row[columns[j]]))
                        fact_obj, is_created = model_fact.objects.get_or_create(gene_dim=gene_dim_obj,
                                                                                person_dim=person_dim_obj)
                        fact_obj.amount = v_
                        fact_obj.save()
                    except Exception as ex:
                        if p_ not in list_:
                            list_.append(p_)
                            print(list_)
        print("\n", "="*100, list_, "\n", "="*100)

            # print(f_, p_, v_)
            # print(n__, max_v, max_d)
        # print(max_v, max_d)
        # print('90121-6 fact')
        log_debug("=== load_file_to_db 101 ===")
        wb.close()
        result = {"status": "ok"}
        return result
