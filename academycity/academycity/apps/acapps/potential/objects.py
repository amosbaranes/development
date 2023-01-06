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
        self.to_save = []
        self.to_save_all = []
        self.save_to_file = None
        self.df_index = None
        self.countries_name = pd.DataFrame(CountryDim.objects.all().values('id', 'country_name'))
        self.measures_name = pd.DataFrame(MeasureDim.objects.all().values('id', 'measure_name'))
        self.options = ["mm", "mx", "xm", "xx"]

    def process_algo(self, dic):
        # print("90060-10 PotentialAlgo: \n", dic, "\n", "="*50)
        wb2 = None
        groups = MeasureGroupDim.objects.all()
        nn__ = 0
        sign_n1 = pd.DataFrame([[0, 0, 0, 0]])
        sign_n2 = pd.DataFrame([[0, 0, 0, 0]])
        sign_n1.columns = self.options
        sign_n2.columns = self.options
        similarity_n1 = pd.DataFrame([[0, 0, 0, 0]])
        similarity_n2 = pd.DataFrame([[0, 0, 0, 0]])
        contribution_n1 = pd.DataFrame([[0, 0, 0, 0]])
        contribution_n2 = pd.DataFrame([[0, 0, 0, 0]])
        relimp_n1 = pd.DataFrame([[0, 0, 0, 0]])
        relimp_n2 = pd.DataFrame([[0, 0, 0, 0]])
        similarity_n1.columns = self.options
        similarity_n2.columns = self.options
        group_d = ""
        for k in groups:
            group = k.group_name
            # print("-"*50)
            # print(group)
            # print("-"*50)
            try:
                self.to_save = []
                self.save_to_file = os.path.join(self.TO_EXCEL, str(dic["time_dim_value"])+"_"+group+"_o.xlsx")
                wb2 = Workbook()
                wb2.save(self.save_to_file)
                wb2.close()
                wb2 = None
                # print("file_path\n", self.save_to_file, "\n", "="*50)
                s = ""
                for v in dic["axes"]:
                    s += "'"+v+"',"
                s += "'"+dic["value"]+"'"
                qs = Fact.objects.filter(measure_dim__measure_group_dim__group_name=group, time_dim_id=dic["time_dim_value"]).all()
                s = "pd.DataFrame(list(qs.values("+s+")))"
                df = eval(s)
                df = df.pivot(index="country_dim", columns='measure_dim', values='amount')
                self.df_index = df.index
                df_columns = df.columns
                df_ = self.add_country_to_df(df)
                self.to_save.append((df_.copy(), 'Data'))
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
                self.add_to_save(title='Normalized-1', a=df_n1, cols=None)
                #
                df_n2 = df_n1.copy()
                df_n2[df_n2 < 0] = 0
                df_n2[df_n2 > 1] = 1
                self.add_to_save(title='Normalized-2', a=df_n2, cols=None)
                #
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
                    self.add_to_save(title='min-max', a=df_1_2, cols=cols)
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
                    a = df_n2.values
                    a_1 = a.copy()
                    a_1 = self.clean_rows(a=a_1, j=1, side="L")
                    a_1 = -1 * a_1.copy()
                    a_1 = self.clean_rows(a=a_1, j=1, side="R")
                    a_1 = -1*a_1
                    a_1.sort(axis=1)                #
                    self.add_to_save(title='Final-1', a=a_1, cols=-1)
                    #
                    a_1 = pd.DataFrame(a_1)
                    a_1.dropna(how='all', axis=1, inplace=True)
                    #
                    a_1 = a_1.apply(self.twenty_rule, axis=1)
                    a_1 = a_1.apply(lambda x: np.sort(x), axis=1, raw=True)
                    self.add_to_save(title='Final-20-rule', a=a_1, cols=-1)

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

                df_1_2.columns = ['min-n1', 'max-n1', 'min-n2', 'max-n2']
                cols = df_1_2.columns
                cols = cols.insert(0, 'country_name')
                self.add_to_save(title='min-max', a=df_1_2, cols=cols)
                # self.add_to_save(title='min-max', a=df_1_2, cols=-1)
                self.save_to_excel_()
            except Exception as ex:
                print(ex)
            df_n1_ = df_n1.copy()
            df_n1_.columns = ['m-'+group, 'x-'+group]
            df_n2_ = df_n2.copy()
            df_n2_.columns = ['m-'+group, 'x-'+group]
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
                group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2, similarity_n1, similarity_n2 =\
                    self.create_similarity(group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2,
                                           similarity_n1, similarity_n2)
                ss_n_mm += '"'+group_d+'-'+group+'-mm",'
                ss_n_mx += '"'+group_d+'-'+group+'-mx",'
                ss_n_xm += '"'+group_d+'-'+group+'-xm",'
                ss_n_xx += '"'+group_d+'-'+group+'-xx",'

        ss_n_mm = ss_n_mm[:-1]
        ss_n_mx = ss_n_mx[:-1]
        ss_n_xm = ss_n_xm[:-1]
        ss_n_xx = ss_n_xx[:-1]

        for n in ["1", "2"]:
            ll = []
            for k in self.options:
                exec("df_n"+n+"_all['d_"+k+"']=df_n"+n+"_all[["+eval("ss_n_"+k)+"]].min(axis=1)")
                exec("ll.append(1-df_n"+n+"_all[["+eval("ss_n_"+k)+"]].min(axis=1).mean())")
            exec("similarity_n"+n+".loc['SComb'] = ll")

            exec("sign_n"+n+".drop([0], axis=0, inplace=True)")
            self.add_to_save_all(title='sign-n'+n, a=eval("sign_n"+n), cols=-1)
            exec("similarity_n"+n+".drop([0], axis=0, inplace=True)")
            self.add_to_save_all(title='similarity-n'+n, a=eval("similarity_n"+n), cols=-1)

        for n in ["1", "2"]:
            nn__ = 0
            for k in groups:
                group = k.group_name
                # print(group)
                if nn__ > 0:
                    ll = []
                    for z in self.options:
                        s_ = "df_n" + n + "_all['dc_"+group+"_" + z + "'] = abs("
                        s_ += "df_n" + n + "_all['d_" + z + "'] - "
                        s_ += "df_n" + n + "_all['" + group_d+"-"+group+"-" + z + "'])"
                        exec(s_)
                        # print('ll.append(1-df_n'+n+'_all["dc_'+group+'_' + z+'"].mean())')
                        exec('ll.append(1-df_n'+n+'_all["dc_'+group+'_' + z+'"].mean())')
                    llc = [x-0.7 for x in ll]
                    llc = llc/sum(llc)
                    exec("contribution_n"+n+".loc[group] = ll")
                    exec("relimp_n"+n+".loc[group] = llc")
                else:
                    nn__ += 1

            self.add_to_save_all(title="all-n"+n, a=eval("df_n"+n+"_all"), cols=-1)
            exec("contribution_n" + n + ".columns = self.options")
            exec("relimp_n" + n + ".columns = self.options")
            exec("contribution_n" + n + ".drop([0], axis=0, inplace=True)")
            exec("relimp_n" + n + ".drop([0], axis=0, inplace=True)")
            # print(eval("contribution_n"+n))
            # print(eval("relimp_n"+n))
            self.add_to_save_all(title='contribution-n'+n, a=eval("contribution_n"+n), cols=-1)
            self.add_to_save_all(title='relimp-n'+n, a=eval("relimp_n"+n), cols=-1)

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
                df_d = eval("abs(df_n"+n+"_all['"+k[0]+"-" + group_d + "'] - df_n"+n+"_all['"+k[1]+"-" + group + "'])")
                # print(df_d.head())
                s_d = df_d.sum()
                # print(s_d)
                df_r = eval("abs(df_n"+n+"_all['"+k[0]+"-" + group_d + "'] - 1 + df_n"+n+"_all['"+k[1]+"-" + group + "'])")
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
            exec("sign_n"+n+".loc[group] = ll")
            exec("similarity_n"+n+".loc[group] = lls")

        return group_d, group, df_n1_all, df_n2_all, df_n1_, df_n2_, sign_n1, sign_n2, similarity_n1, similarity_n2

    def add_country_to_df(self, df, cols=None):
        df_ = df.copy()
        if cols is None:
            # print("BB2")
            cols = ['country_name']
            df_c = df.columns
            for j in df_c:
                k = str(self.measures_name[self.measures_name["id"] == j]["measure_name"]).split("    ")[1].split("\n")[0]
                cols.append(k)
        # print("add_country_to_df", 1)
        df_ = df_.reset_index()
        # print("-"*10, "\nAA\n", "\n", df_)
        df_ = df_.merge(self.countries_name, how='inner', left_on='country_dim', right_on='id').drop(['country_dim', 'id'], axis=1)
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
            with pd.ExcelWriter(self.save_to_file, engine='openpyxl', mode='a') as writer:
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
        with pd.ExcelWriter(self.save_to_file, engine='openpyxl', mode="a") as writer:
            for d in self.to_save:
                try:
                    d[0].to_excel(writer, sheet_name=d[1])
                except Exception as ex:
                    print("9006-3 " + d[2] + str(ex))

        wb = load_workbook(filename=self.save_to_file, read_only=False)
        del wb['Sheet']
        wb.save(self.save_to_file)
        wb.close()

    def save_to_excel_all_(self, year):
        save_to_file_all = os.path.join(self.TO_EXCEL, "all_"+str(year)+".xlsx")
        wb2 = Workbook()
        wb2.save(save_to_file_all)
        wb2.close()

        with pd.ExcelWriter(save_to_file_all, engine='openpyxl', mode="a") as writer:
            for d in self.to_save_all:
                try:
                    d[0].to_excel(writer, sheet_name=d[1])
                except Exception as ex:
                    print("9006-3 " + d[2] + str(ex))

        wb = load_workbook(filename=save_to_file_all, read_only=False)
        del wb['Sheet']
        wb.save(self.save_to_file)
        wb.close()

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
        a.sort(axis=1)
        # if j == 1:
        self.add_to_save(title='Sort '+side+"-"+str(j), a=a, cols=-1)
        #
        a_ = pd.DataFrame(a.copy())
        a_ = a_.loc[a_.apply(lambda x: x.count(), axis=1) > 4]
        a_ = a_.to_numpy()
        # print(a.shape, "\n", a_.shape)
        if a_.shape[0] == 0:
            return a
        d = a[:, 1:2] - a[:, 0:1]
        d_ = a_[:, 1:2] - a_[:, 0:1]
        d_m = np.nanmean(d_, axis=0)
        # print(j, "\n", d_m, "\n", d_m[0])
        if d_m[0] < 0.05:
            #
            df_d = pd.DataFrame(d)
            df_d.index = self.df_index
            df_ = self.add_country_to_df(df_d, cols=-1)
            self.to_save.append((df_.copy(), 'D_'+side+' - '+str(j)))
            # print("d=\n", d)
            #
            b = pd.DataFrame(a.copy())
            b.loc[b.apply(lambda x: x.count(), axis=1) > 4, [0]] = np.nan
            #
            b.index = self.df_index
            df_ = self.add_country_to_df(b, cols=-1)
            self.to_save.append((df_.copy(), side+' b '+str(j)))
            #
            b = b.to_numpy()
            if j+1 < b.shape[1]:
                b = self.clean_rows(b, j+1, side)
        else:
            b = a.copy()
        return b

    def twenty_rule(self, row):
        # print("-1"*10)
        # print(row)
        # print("-2"*10)
        n_row = row.count()
        # print("n_row= ", n_row)
        if n_row < 5:
            n = 0
        elif n_row == 5:
            n = 1
        else:
            n = math.ceil(n_row*0.2)
        min = n_row
        row_best = row
        if n == 0:
            return row_best

        # print("-4"*10)
        # print("n= ", n, "\n range(n+1)=", range(n+1))
        # print("-5"*10)
        for j in range(n+1):
            row_c = row.copy()
            row_c[:j] = np.nan
            # print("-6"*10)
            # print(row_c)
            # print("-7"*10)
            row_c[n_row-(n-j):] = np.nan
            # print(row_c)
            # print("-8"*10)
            # print("max=", row_c.max())
            # print("min=", row_c.min())
            # print("-9"*10)
            if row_c.max()-row_c.min() < min:
                min = row_c.max()-row_c.min()
                row_best = row_c.copy()
        return row_best

    def twentyfive_rule(self, row):
        n_row = row.count()
        row_best = row
        if (n_row > 4) and (row.max()-row.min() > 0.25):
            n = 1
            min = n_row
            for j in range(n+1):
                row_c = row.copy()
                row_c[:j] = np.nan
                row_c[n_row-(n-j):] = np.nan
                if (row_c.max()-row_c.min()) < min :
                    min = row_c.max()-row_c.min()
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

        # files = []
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
            # files.append(f)
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


