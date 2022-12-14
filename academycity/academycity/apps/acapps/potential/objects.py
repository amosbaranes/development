import warnings
import os
from django.conf import settings
from ..ml.basic_ml_objects import BaseDataProcessing
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
from openpyxl import Workbook, load_workbook
import time
from .models import MinMaxCut, MeasureGroupDim, MeasureDim, TimeDim, Fact

from .models import Fact, MinMaxCut, CountryDim

mpl.use('Agg')


class PotentialAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90050-01 PotentialAlgo", dic, '\n', '-'*50)
        super(PotentialAlgo, self).__init__()
        # print("90050-02 PotentialAlgo", dic, '\n', '-'*50)
        self.second_time_save = ''

    def process_algo(self, dic):
        print("90060-10 PotentialAlgo: \n", dic, "\n", "="*50)
        groups = MeasureGroupDim.objects.all()
        # groups = ["GDP"]
        # for group in groups:
        for k in groups:
            group = k.group_name
            # print("-"*50)
            # print(group)
            # print("-"*50)
            try:
                to_save = []
                srr = os.path.join(self.TO_EXCEL, str(dic["time_dim_value"])+"_"+group+"_o.xlsx")
                wb2 = Workbook()
                wb2.save(srr)
                wb2.close()
                wb2 = None
                print("file_path\n", srr, "\n", "="*50)
                s = ""
                for v in dic["axes"]:
                    s += "'"+v+"',"
                s += "'"+dic["value"]+"'"
                qs = Fact.objects.filter(measure_dim__measure_group_dim__group_name=group, time_dim_id=dic["time_dim_value"]).all()
                s = "pd.DataFrame(list(qs.values("+s+")))"
                df = eval(s)
                df = df.pivot(index="country_dim", columns='measure_dim', values='amount')
                dfc = pd.DataFrame(CountryDim.objects.all().values('id', 'country_name'))
                dfm = pd.DataFrame(MeasureDim.objects.all().values('id', 'measure_name'))
                # print("dfc\n", dfc)
                # print(df)
                df_index = df.index
                df_columns = df.columns
                # print("df_columns\n", df_columns, "\n", "="*100)
                print("="*10)
                df_ = self.add_country_to_df(df, dfc, dfm)
                to_save.append((df_.copy(), srr, 'Data'))
                #
                qs_mm = MinMaxCut.objects.filter(measure_dim__measure_group_dim__group_name=group, time_dim_id=dic["time_dim_value"]).all()
                df_mm = pd.DataFrame(list(qs_mm.values('measure_dim', 'min', 'max')))
                first_row = pd.DataFrame(df_mm.T.loc["min"]).T.reset_index().drop(['index'], axis=1)
                first_row.columns = df_columns
                second_row = pd.DataFrame(df_mm.T.loc["max"]).T.reset_index().drop(['index'], axis=1)
                second_row.columns = df_columns
                diff_row = second_row.subtract(first_row, fill_value=None)
                diff_row.columns = df_columns
                # print("6 df_columns\n", df_columns, "\ndiff_row\n", diff_row, "\n", "="*100)
                # print("7 df\n", df, "\n", "="*100)
                df_n1 = df.copy()
                try:
                    df_n1 = df_n1.astype(float)
                except Exception as ex:
                    print("1000: "+str(ex))
                for i, r in df_n1.iterrows():
                    for j in df_columns:
                        try:
                            z = (r[j] - first_row[j].astype(float))/diff_row[j].astype(float)
                            df_n1.loc[i][j] = z
                        except Exception as ex:
                            print("Error i "+str(i)+" "+str(ex))

                # print("1 df_n1\n", df_n1, "\n", "="*100)
                df_n1 = df_n1.apply(pd.to_numeric, errors='coerce').round(6)
                # print("2 df_n1\n", df_n1, "\n", "="*100)
                # self.save_to_excel(df_n1, srr, 'Normalized1')

                df_ = self.add_country_to_df(df_n1, dfc, dfm)
                to_save.append((df_.copy(), srr, 'Normalized1'))
                df_n2 = df_n1.copy()
                df_n2[df_n2 < 0] = 0
                df_n2[df_n2 > 1] = 1
                df_ = self.add_country_to_df(df_n2, dfc, dfm)
                to_save.append((df_.copy(), srr, 'Normalized2'))

                if len(df_n1.columns) < 2:
                    df_n1["max"] = df_n1[df_n1.columns[0]]  # df_n1["Birth Rate"]
                    df_n2["max"] = df_n2[df_n2.columns[0]]  # df_n2["Birth Rate"]
                    df_1_2 = pd.merge(left=df_n1, right=df_n2, left_index=True, right_index=True)
                    df_1_2.columns = ['min-n1', 'max-n1', 'min-n2', 'max-n2']
                    cols = df_1_2.columns
                    cols = cols.insert(0, 'country_name')
                    # print("90876-55\n", cols)
                    df_ = self.add_country_to_df(df_1_2, dfc, dfm, cols)
                    to_save.append((df_.copy(), srr, 'min-max'))
                    # print(to_save)
                    self.save_to_excel_(to_save, srr)
                    # self.save_to_excel(df_1_2, srr, 'min-max')
                    continue
                zero_list = {}
                one_list = {}
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
                        n0.sort()
                        zero_list[i] = n0
                    elif len(n1) > 0:
                        n1.sort()
                        one_list[i] = n1
                a = df_n2.values
                # print('a')
                # print(a)
                a_1 = a.copy()
                a_1 = self.clean_rows(a=a_1,srr=srr,n=0,j=1,to_save=to_save,dfc=dfc,dfm=dfm,df_index=df_index,side="L")
                a_1 = -1 * a_1.copy()
                a_1 = self.clean_rows(a=a_1,srr=srr,n=0,j=1,to_save=to_save,dfc=dfc,dfm=dfm,df_index=df_index,side="R")
                # print(a_1)
                a_1 = -1*a_1
                a_1.sort(axis=1)
                #
                a_1i = pd.DataFrame(a_1)
                a_1i.index = df_index
                df_ = self.add_country_to_df(a_1i, dfc, dfm, cols=-1)
                to_save.append((df_.copy(), srr, 'Final'))
                #

                self.save_to_excel_(to_save, srr)
            except Exception as ex:
                print(ex)

        result = {"status": "ok"}
        return result

    def add_country_to_df(self, df, dfc, dfm, cols=None):
        df_ = df.copy()
        if cols is None:
            # print("BB2")
            cols = ['country_name']
            df_c = df.columns
            for j in df_c:
                k = str(dfm[dfm["id"] == j]["measure_name"]).split("    ")[1].split("\n")[0]
                cols.append(k)
        df_ = df_.reset_index()
        # print("-"*10, "\nAA\n", "\n", df_)
        df_ = df_.merge(dfc, how='inner', left_on='country_dim', right_on='id').drop(['country_dim', 'id'], axis=1)
        # print("BB3\n", "\n", df_)
        c_ = df_.pop('country_name')
        df_.insert(0, 'country_name', c_)
        # print("CC\n", "\n", df_)
        # print("CC1\n", df_.columns, "\n", cols)
        if cols != -1:
            df_.columns = cols
        # print("DD\n", "\n", df_)
        return df_

    def save_to_excel(self, df, srr, folder):
        df2 = df.copy()
        # print(srr + ' -Before sleep save_to_excel- ' + folder)
        total, used, free = shutil.disk_usage("/")
        # print(' total: ' + str(total) + ' used: ' + str(used) + ' free: ' + str(free))
        nnn = 0
        try:
            with pd.ExcelWriter(srr, engine='openpyxl', mode='a') as writer:
                df2.to_excel(writer, sheet_name=folder)
                writer.save()
                time.sleep(5)
            if self.second_time_save != '':
                print("save ok:", self.second_time_save)
            self.second_time_save = ''
            nnn = 1
        except Exception as ee:
            print(ee)
            time.sleep(5)
            self.save_to_excel(df2, srr, folder)
            self.second_time_save = srr
            nnn = 1
        finally:
            if nnn == 0:
                print(srr + ' 55 finally -' + str(nnn) + ' - ' + folder)
                print(srr + ' 55 finally -' + str(nnn) + ' - ' + folder)
                time.sleep(5)
                print(srr + ' 551 finally -' + str(nnn) + ' - ' + folder)
                self.save_to_excel(df2, srr, folder)
                print(srr + ' 66655 finally -' + str(nnn) + ' - ' + folder)
                self.second_time_save = srr

    def save_to_excel_(self, to_save, srr):
        with pd.ExcelWriter(srr, engine='openpyxl', mode="a") as writer:
            for d in to_save:
                try:
                    d[0].to_excel(writer, sheet_name=d[2])
                except Exception as ex:
                    print("9006-3 " + d[2] + str(ex))

    def clean_rows(self, a, srr, n, j, to_save, dfc, dfm, df_index, side="L"):
        try:
            print("j", j)
            if j == 1:
                a.sort(axis=1)
                #
                a_1i = pd.DataFrame(a)
                a_1i.index = df_index
                df_ = self.add_country_to_df(a_1i, dfc, dfm, cols=-1)
                to_save.append((df_.copy(), srr, 'Sort '+side+' - '+str(n)+"-"+str(j)))
            #
            d = a[:, n + j:n + j + 1] - a[:, n:(1+n)]
            #
            df_d = pd.DataFrame(d)
            df_d.index = df_index
            df_ = self.add_country_to_df(df_d, dfc, dfm, cols=-1)
            to_save.append((df_.copy(), srr, 'D_'+side+' - '+str(n)+"-"+str(j)))
            # print("d=\n", d)
            #
            d_m = np.nanmean(d, axis=0)
            print(n, "\n", j, "\n", d.shape[1], "\n", d_m[0])
        except Exception as err:
            print(err)

        b = a.copy()
        if d_m[0] < 0.05:
            b = pd.DataFrame(a.copy())
            b.loc[b.apply(lambda x: x.count(), axis=1) > 4, [(n+j)]] = np.nan
            #
            b.index = df_index
            df_ = self.add_country_to_df(b, dfc, dfm, cols=-1)
            to_save.append((df_.copy(), srr, side+' b '+str(n)+"-"+str(j)))
            #
            b = b.to_numpy()
            # b.sort(axis=1)

        if (n+j+1) < b.shape[1]:
            print((n+j+1), b.shape[1])
            b = self.clean_rows(b, srr, n, j+1, to_save, dfc, dfm, df_index, side)
        return b


class PotentialDataProcessing(BaseDataProcessing, PotentialAlgo):
    def __init__(self, dic):
        # print("90001-00 PotentialDataProcessing", dic, '\n', '-'*50)
        super(PotentialDataProcessing, self).__init__(dic)
        # print("90002-00 PotentialDataProcessing", dic, '\n', '-'*50)
        mdg_fn = "id"
        # try:
        #     mdg_fn = dic["measure_group_dim_field_name"]
        # except Exception as ex:
        #     print("Exc90002-1" + str(ex))
        # mdg_fv = dic["measure_group_dim_field_value"]
        # td_fv = dic["time_dim_value"]
        # # notice in the measure group, we should include index for every category
        # s = 'sq = Fact.objects.filter(measure_dim__measure_group_dim__'+mdg_fn+'='+mdg_fv+', time_dim__id=td_fv)'
        # exec(s)
        # df = pd.DataFrame(sq.values('country_dim', 'measure_dim', 'amount'))
        # print(df)

    def load_file_to_db(self, dic):
        print("90121-1: \n", dic, "="*50)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print('90121-2 dic')
        dic = dic["cube_dic"]
        # print('90121-3 dic', dic)
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_measure_group_dim = apps.get_model(app_label=app_, model_name="measuregroupdim")
        model_min_max_cut = apps.get_model(app_label=app_, model_name="minmaxcut")
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        year = int(self.uploaded_filename.split(".")[0])
        try:
            year_obj, is_created = model_time_dim.objects.get_or_create(id=year)
            if is_created:
                s = 'year_obj.' + dic["dimensions"]["time_dim"]["field_name"]+' = year'
                exec(s)
                year_obj.save()
        except Exception as ex:
            pass

        files = []
        wb = load_workbook(filename=file_path, read_only=False)
        sheet_names = wb.sheetnames
        for f in sheet_names:
            ws = wb[f]
            f = self.clean_name(f)
            try:
                group_obj, is_created = model_measure_group_dim.objects.get_or_create(group_name=f)
                if is_created:
                    group_obj.group_name = f
                    group_obj.save()
            except Exception as ex:
                pass
            files.append(f)
            data = ws.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            # print(columns)
            # Create a DataFrame based on the second and subsequent lines of data
            df = pd.DataFrame(data, columns=columns)
            df = df.reset_index()  # make sure indexes pair with number of rows
            # print(df)
            min_cut = []
            max_cut = []
            for j in range(0, len(columns)):
                min_cut.append(None)
                max_cut.append(None)
            for index, row in df.iterrows():
                if row[1] is not None and str(row[1]) != "None" and str(row[1]) != "":
                    n_ = 0
                    for j in range(1, len(columns)):
                        if str(columns[j]) != "None":
                            n_ += 1
                            f_ = f + str(n_)
                            try:
                                measure_obj, is_created = model_measure_dim.objects.get_or_create(measure_group_dim=group_obj,
                                                                                                  measure_name=f_)
                                if is_created:
                                    measure_obj.measure_code = f_
                                    measure_obj.save()
                            except Exception as ex:
                                pass

                            if row[1] == "Min_Cut" or row[1] == "Max_Cut":
                                # print(columns[j])
                                try:
                                    if row[1] == "Min_Cut":
                                        # print("Min_Cut", row[columns[j]])
                                        min_cut[j] = float(row[columns[j]])
                                    if row[1] == "Max_Cut":
                                        # print("Max_Cut", row[columns[j]])
                                        max_cut[j] = float(row[columns[j]])
                                    if min_cut[j] is not None and max_cut[j] is not None:
                                        # print(f + str(n_), columns[j], "=", min_cut[j], max_cut[j])

                                        try:
                                            min_max_cut_obj, is_created = model_min_max_cut.objects.get_or_create(time_dim=year_obj,
                                                                                                                  measure_dim=measure_obj)
                                            if is_created:
                                                min_max_cut_obj.min = min_cut[j]
                                                min_max_cut_obj.max = max_cut[j]
                                                min_max_cut_obj.save()
                                        except Exception as ex:
                                            pass

                                except Exception as ex:
                                    print(ex)
                            else:
                                try:
                                    country_name = str(row[1]).strip()
                                    country_dim_obj, is_created = model_country_dim.objects.get_or_create(country_name=country_name)
                                    if is_created:
                                        country_dim_obj.country_code = row[1]
                                        country_dim_obj.save()
                                except Exception as ex:
                                    pass
                                try:
                                    v_ = float(str(row[columns[j]]))
                                    if v_ is not None and str(v_) != "nan":
                                        # print(row[columns[j]], float(str(row[columns[j]])))
                                        fact_obj, is_created = model_fact.objects.get_or_create(time_dim=year_obj,
                                                                                                country_dim=country_dim_obj,
                                                                                                measure_dim=measure_obj)
                                        fact_obj.amount = v_
                                        fact_obj.save()
                                except Exception as ex:
                                    print("Error 9055-33: "+str(ex))
        wb.close()

        result = {"status": "ok"}
        return result


