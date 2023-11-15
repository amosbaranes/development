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
        print("90099-99-1000 MMAlgo calculate_min_max_cuts: \n", dic, "\n'", "="*100)

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
            df = df.sort_values(df.columns[0], ascending=False)
            df = df.reset_index()
        except Exception as ex:
            print(ex)

        print(df.head(56),"\n", df.tail(56))
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
            l_ = l/100
            for h in range(int(first_high_group*100), int(step*100), -int(step*100)):
                h_ = (100 - h)/100
                print("-"*30, "\n  h_=", h_, "l_=", l_,"\n","-"*30)

                ll = [h / 100, (100 - l) / 100]
                df_q = df.quantile(ll)
                print("-" * 20)
                print("df_q\n", df_q[["person_dim"]])
                print("-" * 20)
                # print(df_q[["person_dim"]].iloc[0], "\n\n", df_q[["person_dim"]].iloc[1])
                h_cut = (float(df_q[["person_dim"]].iloc[0]) - 1) * (df.shape[0] / (df.shape[0] + 1))
                h_cut = int(round(h_cut))
                print(df.shape, "\nH cut index=", h_cut)
                print("-" * 20)
                cond_h = df.index <= h_cut
                df_h_e = df[cond_h]
                print("Top records sorted by Y:\n", df_h_e.tail(56))
                # print(df_h_e.index)
                # print(len(df_h_e.index)-step_num-1)

                    # n_y = len(df_h_e.index) - step_num - 1
                    # print(n_y)
                    # y_max_cut = df_h_e.iloc[n_y][1]
                    # print("-" * 10, "     H", "     person_index=", df_h_e.iloc[n_y]["person_dim"], "     Y=",
                    #       y_max_cut)

                l_cut = (float(df_q[["person_dim"]].iloc[1]) - 1) * (df.shape[0] / (df.shape[0] + 1))
                l_cut = int(round(l_cut))
                cond_l = df.index > l_cut
                df_l_e = df[cond_l]

                print(df.shape, "\nL cut index=", l_cut)
                print("Low records sorted by Y:\n", df_l_e.head(56))
                    # print(df_l_e.index)

                    # y_min_cut = df_l_e.iloc[step_num][1]
                    # print("-" * 10, "     L", "     person_index=", df_l_e.iloc[step_num]["person_dim"], "     Y=",
                    #       y_min_cut)
                    # print(df_h_e.columns, len(df_h_e.columns))

                nn__ = 0
                nhi_ = 0
                for hi in range(h, int(step*100), -int(step*100)):
                    nhi_ += 1
                    hi_ = (100 - round(hi - step * 100)) / 100
                    n_y_h = int(len(df_h_e.index) - step_num*((hi_-h_)/step))
                    print("h", h_, "h", hi_, "n_y_h=", n_y_h)
                    y_max_cut = df_h_e.iloc[n_y_h][1]
                    nli_ = 0
                    for li in range(l, int(step*100), -int(step*100)):
                        nn__ += 1
                        nli_ += 1
                        li_ = round(li - step*100)/100
                        n_y_l = int(step_num*((l_-li_)/step))
                        # print("l", l_, "li",  li_, "n_y_l", n_y_l)
                        index_ = "h-"+str(h_) + "_" + "l-" + str(l_) + "_" + "hi-" + str(hi_) + "_" + "li-" + str(li_)
                        print("-"*75, "\nindex", index_, "\n", "-"*40)
                        y_min_cut = df_l_e.iloc[n_y_l][1]

                        print("  H", "  person_index=", df_h_e.iloc[n_y_h]["person_dim"], "  Y=",
                              y_max_cut, "           L", "  person_index=", df_l_e.iloc[n_y_l]["person_dim"], "  Y=",
                              y_min_cut)

                        dic_hp[index_] = {}
                        dic_hp[index_]["y"] = {"max_cut": float(y_max_cut), "min_cut": float(y_min_cut)}
                        # print(dic_hp)
                        for gene_num in range(len(df_h_e.columns)-1, 1, -1):
                            # l
                            df_lx = df_l_e[[gene_num]].sort_values(gene_num, ascending=False)
                            # print(df_l_e[[gene_num]], "\n\n")
                            if nn__ < 10:
                                print("Internal Loop: Low range, variable(gene)=", gene_num, "\nsorted values:\n", df_lx)
                            # n_x = len(df_lx.index) - nli_ * step_num - 1
                            n_x = nli_ * step_num
                            # print("n_x=", n_x)
                            # print(df_lx.index)
                            lx = df_lx.iloc[n_x][gene_num]
                            # print(lx)
                            li = pd.DataFrame(df_lx.iloc[n_x])
                            print("Low person index=", li.columns[0], "value=", lx, "\n", "-"*30)

                            # h
                            df_hx = df_h_e[[gene_num]].sort_values(gene_num, ascending=False)
                            # print(df_h_e[[gene_num]], "\n\n")
                            if nn__ < 8:
                                print("Internal Loop: High range, variable(gene)=", gene_num, "\nsorted values:\n", df_hx)

                            n_x = len(df_hx.index) - nhi_ * step_num - 1
                            hx = df_hx.iloc[n_x][gene_num]
                            hi = pd.DataFrame(df_hx.iloc[n_x])
                            print("High person index=", hi.columns[0], "value=", hx, "\n", "-"*30)
                            median_hx = float(df_hx.median())
                            median_lx = float(df_lx.median())
                            print("Low median_lx", median_lx, " High median_hx", median_hx)
                            if median_lx > median_hx:
                                print("Convert Groups:\n AA max_cut", lx, "min_cut", hx)
                                n_x_l = len(df_lx.index) - nli_ * step_num - 1
                                lx_ = df_lx.iloc[n_x_l][gene_num]
                                n_x_h = nhi_ * step_num
                                hx_ = df_hx.iloc[n_x_h][gene_num]

                                lx = hx_
                                hx = lx_

                            if lx > hx:
                                print("BB ", "Max Cut=", hx, "Min Cut=", lx)
                                print("  >> MaxCut lower then MinCut. MinCut=MaxCut=-1 for this index:", index_)
                                dic_hp[index_][gene_num] = {"max_cut": -1, "min_cut": -1}
                                print(" CC max_cut", -1, "min_cut", -1)
                                # else:
                                #     dic_hp[index_][gene_num] = {"max_cut": float(lx), "min_cut": float(hx)}
                            else:
                                print("max_cut", hx, "min_cut", lx)
                                dic_hp[index_][gene_num] = {"max_cut": float(hx), "min_cut": float(lx)}
                print(dic_hp)
                err

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
