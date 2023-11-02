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
        print("90099-99-1000 MMAlgo calculate_min_max_cuts: \n", dic, "\n", "="*50)

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
        # print(df)
        try:
            df = df.pivot(index="person_dim", columns='gene_dim', values='amount')
            df = df.sort_values(df.columns[0], ascending=False)
            df = df.reset_index()
        except Exception as ex:
            print(ex)

        print("="*50)
        print("90-111-2-100\n","\n", df,"\n", df.head(56),"\n", df.tail(56),"\n", df.shape)
        print("="*50)
        step_num = int(df.shape[0]*step)
        print("step_num=", step_num)
        print("="*30)

        # print(range(int(first_high_group*100), 0, -int(step*100)))

        for l in range(int(first_low_group * 100), int((first_low_group-step) * 100), -int(step * 100)):
            l_ = round(l - step*100)/100
            for h in range(int(first_high_group*100), int(step*100), -int(step*100)):
                h_ = (100 - round(h - step*100))/100
                print(l, l_, h, h_)
                ll = [h/100, (100-l)/100]
                print(ll)
                df_q = df.quantile(ll)
                print("-"*20)
                print("df_q\n", df_q[["person_dim"]])
                # print("-"*20)
                # print(df_q[["person_dim"]].iloc[0], "\n\n", df_q[["person_dim"]].iloc[1])
                print(df.shape)
                print("-"*20)
                cond_h = df.index <= int(df_q[["person_dim"]].iloc[0])
                df_h_e = df[cond_h]
                print("Top records sorted by Y:\n", df_h_e.tail(50))
                # print(df_h_e.index)
                print(len(df_h_e.index)-step_num-1)
                print("-"*30, "\nH", "person_index=", df_h_e.iloc[len(df_h_e.index)-step_num-1]["person_dim"],
                      "Y=", df_h_e.iloc[len(df_h_e.index)-step_num-1][1], "\n", "-"*30, "\n")

                cond_l = df.index >= int(df_q[["person_dim"]].iloc[1])
                df_l_e = df[cond_l]
                print("Low records sorted by Y:\n", df_l_e.head(50))
                # print(df_l_e.index)

                print("-"*30, "\nL", "person_index=", df_l_e.iloc[step_num]["person_dim"],
                      "Y=", df_l_e.iloc[step_num][1], "\n", "-"*30, "\n")

                # print(df_h_e.columns, len(df_h_e.columns))
                n_ = 0
                for hi in range(h, 0, -int(step*100)):
                    n_ += 1
                    # print("hi=", hi)
                    for gene_num in range(len(df_h_e.columns)-1, 1, -1):
                        df_x = df_h_e[[gene_num]].sort_values(gene_num, ascending=False)
                        # print(df_h_e[[gene_num]], "\n\n")
                        if n_ == 1:
                            print("\nInternal Loop: variable(gene)=", gene_num, "hi=", hi, "sorted values:\n", df_x, "\n")
                        x = df_x.iloc[len(df_x.index) - n_*step_num - 1][gene_num]
                        i = pd.DataFrame(df_x.iloc[len(df_x.index) - n_*step_num - 1])
                        print(" Internal Loop: variable(gene)=", gene_num, "hi=", hi, "person index=", i.columns[0], "value=", x, "\n", "-"*40, "\n")

                print("="*50)
                print("="*50)
                print("="*50)
        # df = pd.DataFrame(np.array([[1, 10],
        #                             [2, 100],
        #                             [3, 100],
        #                             [4, 100],
        #                             [5, 100],
        #                             [6, 100],
        #                             [7, 100],
        #                             [8, 100],
        #                             [9, 100],
        #                             [10, 100],
        #                             [11, 100],
        #                             [12, 100],
        #                             [13, 100],
        #                             [14, 100],
        #                             [15, 100],
        #                             [16, 100],
        #                             [17, 100],
        #                             [18, 100],
        #                             [19, 100],
        #                             [20, 100],
        #                             [21, 100],
        #                             [22, 100],
        #                             [23, 100],
        #                             [24, 100],
        #                             [25, 100],
        #                             [26, 100],
        #                             [27, 100],
        #                             [28, 100],
        #                             [29, 100],
        #                             [30, 100],
        #                             [31, 100],
        #                             [32, 100],
        #                             [33, 100],
        #                             [34, 100],
        #                             [35, 100],
        #                             [36, 100],
        #                             [37, 100],
        #                             [38, 100],
        #                             [39, 100],
        #                             [40, 100],
        #                             [41, 100],
        #                             [42, 100],
        #                             [43, 100],
        #                             [44, 100],
        #                             [45, 100],
        #                             [46, 100],
        #                             [47, 100],
        #                             [48, 100],
        #                             [49, 100],
        #                             [50, 100],
        #                             [51, 100],
        #                             [52, 100],
        #                             [53, 100],
        #                             [54, 100],
        #                             [55, 100],
        #                             [56, 100],
        #                             [57, 100],
        #                             [58, 100],
        #                             [59, 100],
        #                             [60, 100],
        #                             [61, 100],
        #                             [62, 100],
        #                             [63, 100],
        #                             [64, 100],
        #                             [65, 100],
        #                             [66, 100],
        #                             [67, 100],
        #                             [68, 100],
        #                             [69, 100],
        #                             [70, 100],
        #                             [71, 100],
        #                             [72, 100],
        #                             [73, 100],
        #                             [74, 100],
        #                             [75, 100],
        #                             [76, 100],
        #                             [77, 100],
        #                             [78, 100],
        #                             [79, 100],
        #                             [80, 100],
        #                             [81, 100],
        #                             [82, 100],
        #                             [83, 100],
        #                             [84, 100],
        #                             [85, 100],
        #                             [86, 100],
        #                             [87, 100],
        #                             [88, 100],
        #                             [89, 100],
        #                             [90, 100],
        #                             [91, 100],
        #                             [92, 100],
        #                             [93, 100],
        #                             [94, 100],
        #                             [95, 100],
        #                             [96, 100],
        #                             [97, 100],
        #                             [98, 100],
        #                             [99, 100],
        #                             [100, 100],
        #                             [101, 100],
        #                             [102, 100],
        #                             [103, 100],
        #                             [104, 100],
        #                             [105, 100],
        #                             [106, 100],
        #                             [107, 100],
        #                             [108, 100],
        #                             [109, 100],
        #                             [110, 100],
        #                             [111, 100],
        #                             [112, 100]
        #                             ]),
        #                   columns=['a', 'b'])
        # print(df)
        # print(df.quantile([.4, 0.6]))



                # ll = [l/100, round(h - 100*step)/100]
                # print("ll", ll, "\ndf.quantile(ll)\n", df.quantile(ll))
                # df_q = df.quantile(ll)
                # print("df_q\n", df_q)
                #
                # print("df_q.shape", df_q.shape)
                # print("df_q", df_q)

                # for ih in range(h_, int(step*100), -int(step*100)):
                #     ih_ = round(ih - step*100)/100
                #     print("l", l, "l_", l_, "h_", h_, "ih_", ih_)

        # df_d = ll_dfs[dependent_group]
        # # print(df_d)
        # results = {}
        # best_cut = {"bv": -1}
        #
        # # print("90066-100-5 PotentialAlgo calculate_min_max_cuts: \n", "="*50)
        #
        # for h in high_group_cut:
        #     hh = 1- h

        #     results[hh] = {}
        #     #
        #     # z = 5
        #     # steps_h = list(range(z, 100, z))
        #     # if h == high_group_cut[0]:
        #     #     steps_h.append(95)
        #     # print(h)
        #     steps_h = list(range(5, round(h * 100), 5))
        #     steps_h = [a/100 for a in steps_h]
        #     print("hhhhhhh", h, steps_h)
        #     #
        #     for ll in low_group_cut:
        #         results[hh][ll] = {}
        #         # z_ = 5
        #         # steps_l = list(range(z_, 100, z_))
        #         # if ll == low_group_cut[0]:
        #         #     steps_l.append(95)
        #         steps_l = list(range(5, round(ll * 100), 5))
        #         steps_l = [a/100 for a in steps_l]
        #         print("llllll", ll, steps_l)
        #         #
        #         # print(df_d)
        #         df_q = df_d.quantile([hh, ll])
        #         # print("df_d.shape", df_d.shape)
        #         # print("df_q", df_q)
        #
        #         results[hh][ll][f] = {}
        #         # results[hh][ll][f]["max_cut"] = df_q[f].iloc[0]
        #         # results[hh][ll][f]["min_cut"] = df_q[f].iloc[1]
        #         df_hi = df_d[df_d[f] >= df_q[f].iloc[0]].index
        #         df_li = df_d[df_d[f] <= df_q[f].iloc[1]].index
        #         # print("df", "\n", df_d[df_d[f] >= df_q[f].iloc[0]], "\n\n")
        #         # print("df", "\n", df_d[df_d[f] >= df_q[f].iloc[0]].index, "\n\n")
        #
        #         # print("df", "\n", float(df_d[df_d[f] >= df_q[f].iloc[0]][f].median()), "\n")
        #
        #         # results[hh][ll][f]["max_cut"] = float(df_d[df_d[f] >= df_q[f].iloc[0]][f].median())
        #         # results[hh][ll][f]["min_cut"] = float(df_d[df_d[f] <= df_q[f].iloc[1]][f].median())
        #
        #         for steph in steps_h:
        #             for stepl in steps_l:
        #                 for g in ll_dfs:
        #                     # if g != dependent_group:
        #                     df = ll_dfs[g]
        #                     # print("\n",g, "\n",df.columns)
        #                     iih = []
        #                     iil = []
        #                     for j in df.index:
        #                         if j in df_hi:
        #                             iih.append(j)
        #                         if j in df_li:
        #                             iil.append(j)
        #                     dfh = df.loc[iih]
        #                     dfl = df.loc[iil]
        #
        #                     dfh_q = dfh.quantile(steph/h)
        #                     dfl_q = dfl.quantile((ll-stepl)/ll)
        #                     # print('dfh, dfh', 'steph ', steph, 'dfh_q ', dfh_q)
        #                     # , '\n', 'dfl', dfl, 'stepl', stepl, 'dfl_q', dfl_q)
        #
        #                     if steph not in results[hh][ll][f]:
        #                         results[hh][ll][f][steph] = {}
        #                     if stepl not in results[hh][ll][f][steph]:
        #                         results[hh][ll][f][steph][stepl] = {}
        #                         results[hh][ll][f][steph][stepl]["groups"] = {}
        #                     if g not in results[hh][ll][f][steph][stepl]["groups"]:
        #                         results[hh][ll][f][steph][stepl]["groups"][g] = {}
        #
        #                     for k in df.columns:
        #                         # print(steph, stepl, k, dfh_q[k], dfl_q[k])
        #                         dfh_ik = dfh[dfh[k] >= dfh_q[k]][k]
        #                         dfl_ik = dfl[dfl[k] <= dfl_q[k]][k]
        #                         # print('dfh[dfh[k] >= dfh_q[k]]', dfh[dfh[k] >= dfh_q[k]].index, 'dfh_ik.median()', dfh_ik.median(), 'dfl_ik.median()', dfl_ik.median())
        #                         # print('g, k, dfh_ik.shape', g, k, dfh_ik.shape)
        #                         if dfh_ik.shape == 0 or dfl_ik.shape == 0:
        #                             continue
        #                         results[hh][ll][f][steph][stepl]["groups"][g][k] = eval('{"min_cut": dfl_ik.'+l_method+'(), "max_cut": dfh_ik.'+u_method+'()}')
        #                 # print(results)
        #                 dic = {"dependent_group": dependent_group, "f":f, "steph":steph, "stepl":stepl,
        #                        "df_d": df_d, "ll_dfs": ll_dfs, "groups": results[hh][ll][f]}
        #                 bv = self.get_similarity(dic)
        #                 if bv > best_cut["bv"]:
        #                     best_cut = {"bv": bv, "hh": hh, "ll": ll, "steph":steph, "stepl":stepl, "f":f,
        #                                 "dependent_group": dependent_group, "year": year_,
        #                                 "f_groups":results[hh][ll][f][steph][stepl]["groups"]}
        #
        #                     # print('best_cut\n', 'hh', hh, 'll', ll, 'results 1 steph', steph, 'stepl', stepl, "dv", bv, "\n",
        #                     #       best_cut)
        #                 print('hh', hh, 'll', ll, 'steph', round(100*(steph+hh))/100, 'stepl', round(100*(ll-stepl))/100, 'dv', bv, 'best', best_cut['bv'])
        #
        # # print("="*100)
        # best_cut["df_d"] = df_d
        # # print("final", best_cut, "="*100)
        # #
        # file_path = os.path.join(self.PICKLE_PATH, "result_"+str(f)+"_"+year_+".pkl")
        # print(file_path)
        # with open(file_path, 'wb') as handle:
        #     pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # file_path = os.path.join(self.PICKLE_PATH, "best_cut_"+str(f)+"_"+year_+".pkl")
        # print(file_path)
        # with open(file_path, 'wb') as handle:
        #     pickle.dump(best_cut, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #
        # # # #
        # print("=" * 100)
        # #

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
