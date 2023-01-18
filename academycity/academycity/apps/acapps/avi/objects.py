import warnings
import os
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
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
#
from .models import TimeDim, CountryDim, MeasureDim, WorldBankFact
#
import pandas as pd
import numpy as np
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from django.apps import apps


class AviDataProcessing(BaseDataProcessing, BasePotentialAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def check_country(self, cc):
        if cc == "Viet Nam":
            cc = "Vietnam"
        elif cc == "Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "DR Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "Congo":
            cc = "Republic of the Congo"
        elif cc == "Democratic Republic Of The Congo":
            cc = "Democratic Republic of the Congo"
        elif cc == "Russian Federation":
            cc = "Russia"
        elif cc == "Côte d’Ivoire":
            cc = "Cote d'Ivoire"
        elif cc == "Eswatini (Swaziland)":
            cc = "Eswatini"
        elif cc == "Slovak Republic":
            cc = "Slovakia"
        elif cc == "Korea":
            cc = "South Korea"
        elif cc == "Republic Of Korea":
            cc = "South Korea"
        elif cc == "Korea, Dem. People's Rep":
            cc = "North Korea"
        elif cc == "United States Of America":
            cc = "United States"
        elif cc == "Cabo Verde":
            cc = "Cape Verde"
        elif cc == "United Republic Of Tanzania":
            cc = "Tanzania"
        elif cc == "Guinea Bissau":
            cc = "Guinea-bissau"
        elif cc == "Lao People's Democratic Republic":
            cc = "Laos"
        elif cc == "Republic Of Moldova":
            cc = "Moldova"
        elif cc == "Republic Of North Macedonia":
            cc = "North Macedonia"
        elif cc == "Macedonia":
            cc = "North Macedonia"
        elif cc == "EU (27)":
            cc = "EU27"
        elif cc == "Yemen, Rep.":
            cc = "Yemen"
        elif cc == "Venezuela, RB":
            cc = "Venezuela"
        elif cc == "turkiye":
            cc = "turkey"
        elif cc == "Egypt, Arab Rep.":
            cc = "Egypt"
        elif cc == "China (Mainland)":
            cc = "China"
        elif cc == "Hong Kong SAR":
            cc = "China-Hong Kong"
        elif cc == "Hong Kong (China)":
            cc = "China-Hong Kong"
        elif cc == "Hong Kong":
            cc = "China-Hong Kong"
        elif cc == "USA":
            cc = "United States"
        elif cc == "Slovak Republic":
            cc = "Slovakia"
        elif cc == "Macau":
            cc = "China-Macau"
        elif cc == "Cabo Verde":
            cc = "Cape Verde"
        elif cc == "United Republic Of Tanzania":
            cc = "Tanzania"
        elif cc == "Guinea Bissau":
            cc = "Guinea-bissau"
        elif cc == "Republic Of Moldova":
            cc = "Moldova"
        return cc

    # _1
    def load_wbfile_to_db(self, dic):
        print("90121-5: \n", dic, "="*50)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        for index, row in df.iterrows():
            print(row["Country Name"], row["Country Code"], row["Series Name"], row["Series Code"])
            # Country
            try:
                c, is_created = model_country_dim.objects.get_or_create(country_code=row["Country Code"])
                if is_created:
                    cc = self.check_country(row["Country Name"])
                    s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = "' + cc + '"'
                    exec(s)
                    c.save()
            except Exception as ex:
                print("90987-1 Error measure:"+str(ex))
            #
            if row["Series Name"] == "GDP per capita (constant 2015 US$)":
                measure_name = "GDPPC2015$"
                group_measure_name = "Economics"
            elif row["Series Name"] == "Population, total":
                measure_name = "TotalPop"
                group_measure_name = "General"
            print(group_measure_name, measure_name)
            #
            try:
                gm, is_created = model_group_measure_dim.objects.get_or_create(group_name=group_measure_name)
                mm = row["Series Code"]
                m, is_created = model_measure_dim.objects.get_or_create(measure_code=mm, measure_group_dim=gm)
                if is_created:
                    s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = "' + measure_name + '"'
                    exec(s)
                    m.save()
            except Exception as ex:
                print("90986-1 Error measure:"+str(ex))

            for j in range(4, len(df.columns)):
                k = df.columns[j]
                try:
                    if float("{:.2f}".format(row[k])) > 0 or float("{:.2f}".format(row[k])) < 0:
                        s = k.split(" ")
                        # print(s[0])
                        yy = int(s[0])
                        t, is_created = model_time_dim.objects.get_or_create(id=yy)
                        if is_created:
                            # t.year = yy
                            s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                            # print(s)
                            exec(s)
                            t.save()

                        a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
                        if is_created:
                            # a.amount = float(row[k])
                            s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(float("{:.2f}".format((row[k]))))
                            # print(s)
                            exec(s)
                            a.save()
                except Exception as ex:
                    pass
                    # print(k, row[k], "9065-55 Error: "+str(ex))

        result = {"status": "ok"}
        return result

    # _2
    def load_oecdfile_to_db(self, dic):
        print("90123-5: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)

        for index, row in df.iterrows():
            if row["Measurement"] == "number of AI Research Publication":
                measure_name = "OECD#AIRePub"
                group_measure_name = "AIRePub"
                country_field = "country_code"
            elif row["Measurement"] == "Total number of number of All Research Publication":
                measure_name = "OECD#AllRePub"
                group_measure_name = "AllRePub"
                country_field = "country_code"
            elif row["Measurement"] == "AI publications":
                measure_name = "OECD#AIPub"
                group_measure_name = "AIPub"
                country_field = "country_name"

            try:
                if str(row["Value"]) != "nan":
                    if float("{:.2f}".format((row["Value"]))) > 0 or float("{:.2f}".format((row["Value"]))) < 0:
                        gm, is_created = model_group_measure_dim.objects.get_or_create(group_name=group_measure_name)
                        # year
                        try:
                            yy = int(row["Year"])
                            t, is_created = model_time_dim.objects.get_or_create(id=yy)
                            if is_created:
                                # t.year = yy
                                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                                # print(s)
                                exec(s)
                                t.save()
                        except Exception as ex:
                            pass
                        # country
                        try:
                            cc = row["Country"]
                            if country_field == "country_code":
                                c, is_created = model_country_dim.objects.get_or_create(country_code=cc)
                            else:
                                cc = self.check_country(cc)
                                c, is_created = model_country_dim.objects.get_or_create(country_name=cc)
                            if is_created:
                                # c.country_name = cc
                                print(cc)
                                s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = cc'
                                # print(s)
                                exec(s)
                                c.save()
                        except Exception as ex:
                            pass
                        # measure
                        try:
                            mm = measure_name
                            # print(cc, yy, mm)
                            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm, measure_group_dim=gm)
                            if is_created:
                                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                                exec(s)
                                m.save()
                        except Exception as ex:
                            pass
                        # print("9075-33")
                        # print(t, c, m)
                        a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
                        if is_created:
                            # a.amount = float("{:.2f}".format((row["Value"])))
                            s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(float("{:.2f}".format((row["Value"]))))
                            # print(s)
                            exec(s)
                            a.save()
            except Exception as ex:
                print("90652-3" + str(ex))

        result = {"status": "ok"}
        return result

    # 1
    def load_ai_shanghai_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        match = {"101-150":24, "151-200":22, "201-300":20, "301-400":18, "401-500":16,
                 "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}
        #
        df_cc = pd.read_excel(os.path.join(self.target_folder, "countries.xlsx"), sheet_name="Data", header=0)
        # print(df_cc)
        #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        yy = int(file_path.split("_")[2].split(".")[0])
        print(yy)
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass
        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="Edu")
            mm = "shanghai"
            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm,
                                                                    measure_group_dim=gm)
            if is_created:
                # m.measure_code = mm
                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                # print(s)
                exec(s)
                m.save()
        except Exception as ex:
            print("9022-2 Error measure:"+str(ex))
        with open(file_path) as f:
            soup = BeautifulSoup(f.read())
            tbody_tag = soup.find('tbody')
            try:
                rows = tbody_tag.find_all('tr')
                # print(rows)
                for row in rows:
                    try:
                        cells = row.find_all('td')
                        cc_ = cells[2].find('div')["style"].split("/")[4].split(".")[0]
                        cc_ = self.check_country(cc_)
                        sn = cells[0].find('div').text.strip()
                        uu = cells[1].find('span', class_='univ-name').text.strip()
                        sg = cells[4].text.strip()
                        # print(uu, sg)
                        if len(sn)>3:
                            sg = match[sn]
                        # print(cc_, sn, uu, sg)
                        try:
                            try:
                                try:
                                    cc = df_cc[df_cc["cc"]==cc_]["country"].item()
                                except Exception as ex:
                                    print("9087-88 Error country="+cc_+str(ex), uu)
                                    continue

                                c, is_created = model_country_dim.objects.get_or_create(country_name=cc)
                                if is_created:
                                    s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = cc'
                                    c.cc = cc_
                                    c.country_code = cc_
                                    c.country_name = cc
                                    # exec(s)
                                    c.save()
                            except Exception as ex:
                                print("Error country 9080-1: " + str(ex))
                            try:
                                u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                           country_dim=c)
                                if is_created:
                                    # t.year = yy
                                    s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                    # print(s)
                                    exec(s)
                                    u.save()
                            except Exception as ex:
                                pass
                            a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c,
                                                                             university_dim=u, measure_dim=m)
                            if is_created:
                                s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(sg)
                                # print(s)
                                exec(s)
                                a.save()

                        except Exception as ex:
                            print("9085-7 Error university: "+uu+" " +str(ex))
                            continue
                    except Exception as ex:
                        pass
            except Exception as ex:
                print("Error 9070-1"+str(ex))

        # update worldBankFact
        qs = model_fact.objects.all()
        df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
        print(df)
        df = df.pivot_table(values='amount', index='country_dim_id', columns=['time_dim_id', 'measure_dim_id'],
                            aggfunc='sum')
        # print(df)
        for k in df.columns:
            tid = k[0]
            mid = k[1]
            df_ = df[k[0]][k[1]]
            df_ = df_.reset_index()
            # print(df_)
            for i, r in df_.iterrows():
                # print(r)
                cid = r["country_dim_id"]
                if str(r[mid]) != "nan":
                    # print("=1"*50)
                    # print(r[mid])
                    amount = r[mid]

                    # print(tid, type(tid), mid, type(tid), cid)
                    t = model_time_dim.objects.get(id=tid)
                    c = model_country_dim.objects.get(id=cid)
                    m=model_measure_dim.objects.get(id=mid)
                    f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                    if cr:
                        f.amount = amount
                        f.save()

        result = {"status": "ok"}
        return result

    # 2
    def load_ai_shanghai_engineering_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        match = {"101-150":24, "151-200":22, "201-300":20, "301-400":18, "401-500":16,
                 "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}
        #
        # df_cc = pd.read_excel(os.path.join(self.target_folder, "countries.xlsx"), sheet_name="Data", header=0)
        # print(df_cc)
        #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        yy = int(file_path.split("_")[2].split(".")[0])
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass
        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="EduEng")
            mm = "shanghaiEng"
            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm,
                                                                    measure_group_dim=gm)
            if is_created:
                # m.measure_code = mm
                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                # print(s)
                exec(s)
                m.save()
        except Exception as ex:
            print("9023-3 Error measure:"+str(ex))
        with open(file_path) as f:
            soup = BeautifulSoup(f.read())
            try:
                rows = soup.find_all('div', {"class": "row ind"})
                n_=0
                for row in rows:
                    try:
                        # print(row)
                        n_+=1
                        sn = row.find("div", class_= "_univ-rank").text.strip()
                        uu = row.find("div", class_= "td-wrap").text.strip()
                        sg = row.find("span", class_= "overall-score-span").text.strip()
                        cc_ = row.find("div", class_= "location").text.strip().split(",")[1].strip()
                        # print(n_, uu, "="+sg+"=", cc_)
                        if sg.strip() == "-":
                            if n_ < 151:
                                sn = "101-150"
                            elif n_ < 201:
                                sn = "151-200"
                            elif n_ < 301:
                                sn = "201-300"
                            elif n_ < 401:
                                sn = "301-400"
                            elif n_ < 501:
                                sn = "401-500"
                            elif n_ < 601:
                                sn = "501-600"
                            elif n_ < 701:
                                sn = "601-700"
                            elif n_ < 801:
                                sn = "701-800"
                            elif n_ < 901:
                                sn = "801-900"
                            elif n_ < 1001:
                                sn = "901-1000"
                            sg = match[sn]
                            # print(sn, sg)
                        # print(len(sn), uu, sg, cc_)

                        try:
                            try:
                                cc_ = self.check_country(cc_)
                                c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                                if is_created:
                                    c.country_name = cc_
                                    c.country_code = cc_
                                    c.country_cc = cc_
                                    c.save()
                            except Exception as ex:
                                print("Error country 9080-1: " + str(ex))
                            try:
                                u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                           country_dim=c)
                                if is_created:
                                    print(uu)
                                    s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                    # print(s)
                                    exec(s)
                                    u.save()
                            except Exception as ex:
                                pass
                            a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c,
                                                                             university_dim=u, measure_dim=m)
                            if is_created:
                                s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(sg)
                                # print(s)
                                exec(s)
                                a.save()

                        except Exception as ex:
                            print("9085-7 Error university: "+uu+" " +str(ex))
                            continue
                    except Exception as ex:
                        pass
            except Exception as ex:
                print("Error 9070-1"+str(ex))

        # update worldBankFact
        qs = model_fact.objects.filter(measure_dim__measure_name=mm).all()
        df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
        # print(df)
        df = df.pivot_table(values='amount', index='country_dim_id', columns=['time_dim_id', 'measure_dim_id'],
                            aggfunc='sum')
        # print(df)
        for k in df.columns:
            tid = k[0]
            mid = k[1]
            df_ = df[k[0]][k[1]]
            df_ = df_.reset_index()
            # print(df_)
            for i, r in df_.iterrows():
                # print(r)
                cid = r["country_dim_id"]
                if str(r[mid]) != "nan":
                    # print("=1"*50)
                    # print(r[mid])
                    amount = r[mid]

                    # print(tid, type(tid), mid, type(tid), cid)
                    t = model_time_dim.objects.get(id=tid)
                    c = model_country_dim.objects.get(id=cid)
                    m=model_measure_dim.objects.get(id=mid)
                    f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                    if cr:
                        f.amount = amount
                        f.save()

        result = {"status": "ok"}
        return result

    # 3
    def load_ai_cwur_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        match = {"101-150":24, "151-200":22, "201-300":20, "301-400":18, "401-500":16,
                 "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}
        # #
        # df_cc = pd.read_excel(os.path.join(self.target_folder, "countries.xlsx"), sheet_name="Data", header=0)
        # # print(df_cc)
        # #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)

        yy = int(file_path.split("_")[1].split(".")[0])
        print(yy)

        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass

        try:
            if yy in [2017]:
                llg = [12]
                ll = ["score"]
                llgm = ["Edu"]
            elif yy in [2018]:
                llg = [7, 11]
                ll = ["research", "score"]
                llgm = ["EduRes", "Edu"]
            else:
                llg = [7, 8]
                ll = ["research", "score"]
                llgm = ["EduRes", "Edu"]
            nll_ = len(ll)
            for jj in range(nll_):
                k = ll[jj]
                gm, is_created = model_group_measure_dim.objects.get_or_create(group_name=llgm[jj])
                smm = "cwur"+k
                # print(smm)
                s = "mm"+k+", is_created = model_measure_dim.objects.get_or_create(measure_name='"+smm+"', measure_group_dim=gm)"
                # print(s)
                exec(s)
                if is_created:
                    s = 'mm'+k+'.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = '+smm
                    # print(s)
                    exec(s)
                    m.save()
        except Exception as ex:
            print("9028-8 Error measure:"+str(ex))
        with open(file_path) as f:
            soup = BeautifulSoup(f.read())
            tbody_tag = soup.find('tbody')
            try:
                rows = tbody_tag.find_all('tr')
                # print(rows)
                for row in rows:
                    try:
                        # print(row)
                        cells = row.find_all('td')
                        uu = cells[1].find('a').text.strip()
                        if yy in [2017, 2018]:
                            cc_ = cells[2].find('a').text.strip()
                        else:
                            cc_ = cells[2].text.strip()
                        # print(uu, cc_)

                        nll = len(ll)
                        for i in range(nll):
                            # smm = "cwur" + k
                            sg = cells[llg[i]].text.strip()
                            # print("A\n", "="*10)
                            # print(sg)
                            # print(cc_, sn, uu, sg)
                            try:
                                try:
                                    cc_ = self.check_country(cc_)
                                    c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                                    if is_created:
                                        print("="*50)
                                        print(cc_)
                                        print("="*50)
                                        c.country_cc = cc_
                                        c.country_code = cc_
                                        c.country_name = cc_
                                        c.save()
                                except Exception as ex:
                                    print("Error country 9080-1: " + str(ex))
                                try:
                                    u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                               country_dim=c)
                                    if is_created:
                                        s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                        # print(s, "\n", uu)
                                        exec(s)
                                        u.save()
                                except Exception as ex:
                                    pass
                                 # print(s)
                                # exec(s)
                                try:
                                    if sg == "> 1000":
                                        sg = 1000
                                    kkk = float(sg)
                                    a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c,
                                                                                     university_dim=u,
                                                                                     measure_dim=eval("mm" + ll[i]))
                                    a.amount = kkk
                                    a.save()
                                except Exception as ex:
                                    pass
                                # print("="*10)

                            except Exception as ex:
                                print("9085-7 Error university: "+uu+" " +str(ex))
                                continue
                    except Exception as ex:
                        pass
            except Exception as ex:
                print("Error 9070-1"+str(ex))

        # update worldBankFact
        print("="*50, "\n","move data to fact table\n", t, "\n", "="*50)
        nll_ = len(ll)
        for jj in range(nll_):
            j = ll[jj]
            try:
                # print("="*100, "\n", j, "\n", "="*100)
                mm = eval("mm" + j)
                qs = model_fact.objects.filter(measure_dim__measure_name=mm, time_dim=t).all()
                df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
                # print("A\n", "="*10, "\n", df)
                df = df.pivot_table(values='amount', index='country_dim_id', columns=['time_dim_id', 'measure_dim_id'],
                                aggfunc='sum')
                # print("B\n", "="*10, "\n", df)
                for k in df.columns:
                    tid = k[0]
                    mid = k[1]
                    df_ = df[k[0]][k[1]]
                    df_ = df_.reset_index()
                    # print("C\n", "=" * 10, "\n", df_)
                    for i, r in df_.iterrows():
                        # print(r)
                        cid = r["country_dim_id"]
                        if str(r[mid]) != "nan":
                            # print("=1"*50)
                            # print(r[mid])
                            amount = -1
                            try:
                                amount = r[mid]
                            except Exception as ex:
                                print("9077-77 Error "+ str(ex))
                            if amount == -1:
                                continue
                            # print(tid, type(tid), mid, type(tid), cid)
                            t = model_time_dim.objects.get(id=tid)
                            c = model_country_dim.objects.get(id=cid)
                            m=model_measure_dim.objects.get(id=mid)
                            try:
                                # print("D\n", "=" * 10, "\n", "DDDDD", yy, t, c, m)
                                f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                                # print("E\n", "=" * 10, "\n", "EEEEE", f, cr)
                                if cr:
                                    # print("F\n", "=" * 10, "\n", "FFFFFF", amount)
                                    f.amount = amount
                                    f.save()
                            except Exception as ex:
                                print("9088-88 Error "+ str(ex))

                # print("=" * 150, "\n", j, "\n", "=" * 150)
                # print("=" * 150, "\n", j, "\n", "=" * 150)
            except Exception as ex:
                print("9066-66 Error "+ str(ex))

        result = {"status": "ok"}
        return result

    def load_ai_oxford_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)

        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)

        yy = int(file_path.split("_")[1].split(".")[0])
        print("="*100)
        print(yy)
        print("="*100)
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass
        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="GovAI")
            print(gm)
            mm = "oxford"
            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm, measure_group_dim=gm)
            if is_created:
                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                exec(s)
                m.save()
        except Exception as ex:
            print("9024-4 Error measure:"+str(ex))

        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print("A\n", df)
        for i, r in df.iterrows():
            # print(r)
            cc_ = r["country"]
            sg = r["score"]
            try:
                # print("=" * 100)
                # print(cc_)
                cc__ = cc_.split(" ")
                # print(cc__)
                n_ = len(cc__)
                for j in range(n_):
                    cc__[j] = cc__[j].capitalize()
                # print(cc__)
                cc_ = ' '.join(cc__).strip()
                # print(cc_)
                # print("="*100)
                cc_ = self.check_country(cc_)
                c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                if is_created:
                    print(cc_)
                    c.country_name = cc_
                    c.country_code = cc_
                    c.country_cc = cc_
                    c.save()
            except Exception as ex:
                print("Error country 9080-1: " + str(ex))
            amount = -1
            try:
                amount = float(r["score"])
                # print(amount)
                if amount > -1:
                    f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                    if cr:
                        f.amount = float(amount)
                        f.save()
            except Exception as ex:
                print("9060-60 Error: ", str(ex))

        result = {"status": "ok"}
        return result

    def load_ai_oxford22_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)

        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)

        yy = int(file_path.split("_")[1].split(".")[0])
        # print("="*100)
        # print(yy)
        # print("="*100)
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass
        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="GovAI")
            mm = "oxford"
            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm, measure_group_dim=gm)
            if is_created:
                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                exec(s)
                m.save()
        except Exception as ex:
            print("90261-5 Error measure:"+str(ex))

        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print("A\n", df)

        for i, r in df.iterrows():
            # print(r)
            s = r["data"]
            ns1 = 0
            ns2 = 0
            for h in range(2, 200):
                # print("h=", h)
                if h > 2:
                    ns1 = ns2 + 1
                else:
                    ns1 = ns2
                ns2 = s.find(" "+str(h)+" ")
                if ns2 < 0:
                    break
                # print("ns1, ns2=", ns1, ns2)
                si = s[ns1:ns2]
                # print(si)
                llsi = si.split(" ")
                # print(llsi)
                nl = len(llsi)
                nc = nl - 4
                cc_ = ' '.join(llsi[1:nc]).strip()
                sg = llsi[len(llsi)-4]
                # print(cc_, sg)
                try:
                    # print("=" * 100)
                    # print(cc_)
                    cc__ = cc_.split(" ")
                    # print(cc__)
                    n_ = len(cc__)
                    for j in range(n_):
                        cc__[j] = cc__[j].capitalize()
                    # print(cc__)
                    cc_ = ' '.join(cc__).strip()
                    # print(cc_)
                    # print("="*100)

                    cc_ = self.check_country(cc_)
                    c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                    if is_created:
                        print(cc_)
                        c.country_name = cc_
                        c.country_code = cc_
                        c.country_cc = cc_
                        c.save()
                except Exception as ex:
                    print("Error country 9080-1: " + str(ex))
                amount = -1
                try:
                    amount = float(sg)
                    # print(amount)
                    if amount > -1:
                        f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                        if cr:
                            f.amount = float(amount)
                            f.save()
                except Exception as ex:
                    print("9060-60 Error: ", str(ex))

        result = {"status": "ok"}
        return result

    def load_ai_the_reputation_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        # match = {'51-60''':5, '61-70''':4, '71-80':3, '81–90':2, '91–100':1}
        #                  # "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}
        # print(match)
        # print(match["91-100"])
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        yy = int(file_path.split("_")[1].split(".")[0])
        print(yy)
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass
        if yy in [2017, 2018]:
            llg = [2, 3]
            ll = ["research", "score"]
            llgm = ["EduRes", "Edu"]
        else:
            llg = [2, 3]
            ll = ["research", "score"]
            llgm = ["EduRes", "Edu"]

        print(ll, llg, llgm)
        try:
            nll_ = len(ll)
            for jj in range(nll_):
                k = ll[jj]
                gm, is_created = model_group_measure_dim.objects.get_or_create(group_name=llgm[jj])
                smm = "the"+k
                # print(smm)
                s = "mm"+k+", is_created = model_measure_dim.objects.get_or_create(measure_name='"+smm+"', measure_group_dim=gm)"
                # print(s)
                exec(s)
                if is_created:
                    s = 'mm'+k+'.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = '+smm
                    # print(s)
                    exec(s)
                    m.save()
        except Exception as ex:
            print("9025-5 Error measure:"+str(ex))

        with open(file_path) as f:
            soup = BeautifulSoup(f.read())
            tbody_tag = soup.find('tbody')
            try:
                rows = tbody_tag.find_all('tr')
                # print(rows)
                for row in rows:
                    try:
                        # print(row)
                        cells = row.find_all('td')
                        uu = cells[1].find('a').text.strip()
                        cc_ = cells[1].find('div', class_='location').find('a').text.strip()
                        # print(uu, cc_)

                        nll = len(ll)
                        for i in range(nll):
                            # smm = "cwur" + k
                            sg = cells[llg[i]].text.strip()
                            # print("A\n", "="*10)
                            if sg.strip() == "_" or sg.strip() == "-":
                                rk = str(cells[0].text.strip())
                                # print(rk)
                                if rk == '51–60' or rk == '51-60':
                                    sg = 5
                                elif rk == '61–70' or rk == '61-70':
                                    sg = 4
                                elif rk == '71–80' or rk == '71-80':
                                    sg = 3
                                elif rk == '81–90' or rk == '81-90':
                                    sg = 2
                                elif rk == '91–100' or rk == '91-100':
                                    sg = 1
                                elif rk == '101-125' or rk == '101-125':
                                    sg = 0.75
                                elif rk == '126-150' or rk == '126-150':
                                    sg = 0.5
                                elif rk == '151-175' or rk == '151-175':
                                    sg = 0.25
                                elif rk == '176-200' or rk == '176-200':
                                    sg = 0.1
                            print(cc_, uu, sg)
                            try:
                                try:
                                    cc_ = self.check_country(cc_)
                                    c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                                    if is_created:
                                        print("="*50)
                                        print(cc_)
                                        print("="*50)
                                        c.country_cc = cc_
                                        c.country_code = cc_
                                        c.country_name = cc_
                                        c.save()
                                except Exception as ex:
                                    print("Error country 9080-1: " + str(ex))
                                try:
                                    u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                               country_dim=c)
                                    if is_created:
                                        s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                        print(s, "\n", uu)
                                        exec(s)
                                        u.save()
                                except Exception as ex:
                                    pass
                                 # print(s)
                                # exec(s)
                                try:
                                    kkk = float(sg)
                                    a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c,
                                                                                     university_dim=u,
                                                                                     measure_dim=eval("mm" + ll[i]))
                                    a.amount = kkk
                                    a.save()
                                except Exception as ex:
                                    pass
                                # print("="*10)

                            except Exception as ex:
                                print("9085-7 Error university: "+uu+" " +str(ex))
                                continue
                    except Exception as ex:
                        pass
            except Exception as ex:
                print("Error 9070-1"+str(ex))

        # update worldBankFact
        print("="*50, "\n","move data to fact table\n", t, "\n", "="*50)
        nll_ = len(ll)
        for jj in range(nll_):
            j = ll[jj]
            try:
                print("="*100, "\n", j, "\n", "="*100)
                mm = eval("mm" + j)
                qs = model_fact.objects.filter(measure_dim__measure_name=mm, time_dim=t).all()
                df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
                # print("A\n", "="*10, "\n", df)
                df = df.pivot_table(values='amount', index='country_dim_id', columns=['time_dim_id', 'measure_dim_id'],
                                aggfunc='sum')
                # print("B\n", "="*10, "\n", df)
                for k in df.columns:
                    tid = k[0]
                    mid = k[1]
                    df_ = df[k[0]][k[1]]
                    df_ = df_.reset_index()
                    # print("C\n", "=" * 10, "\n", df_)
                    for i, r in df_.iterrows():
                        # print(r)
                        cid = r["country_dim_id"]
                        if str(r[mid]) != "nan":
                            # print("=1"*50)
                            # print(r[mid])
                            amount = -1
                            try:
                                amount = r[mid]
                            except Exception as ex:
                                print("9077-77 Error "+ str(ex))
                            if amount == -1:
                                continue
                            # print(tid, type(tid), mid, type(tid), cid)
                            t = model_time_dim.objects.get(id=tid)
                            c = model_country_dim.objects.get(id=cid)
                            m=model_measure_dim.objects.get(id=mid)
                            try:
                                # print("D\n", "=" * 10, "\n", "DDDDD", yy, t, c, m)
                                f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                                # print("E\n", "=" * 10, "\n", "EEEEE", f, cr)
                                if cr:
                                    # print("F", amount)
                                    f.amount = amount
                                    f.save()
                            except Exception as ex:
                                print("9088-88 Error "+ str(ex))

                # print("=" * 150, "\n", j, "\n", "=" * 150)
                # print("=" * 150, "\n", j, "\n", "=" * 150)
            except Exception as ex:
                print("9066-66 Error "+ str(ex))

        result = {"status": "ok"}
        return result

    def load_ai_research_engineering_technology_file_to_db(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        match = {"101-150":24, "151-200":22, "201-300":20, "301-400":18, "401-500":16,
                 "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}

        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        yy = int(file_path.split("_")[1].split(".")[0])
        print(yy)
        try:
            t, is_created = model_time_dim.objects.get_or_create(id=yy)
            if is_created:
                # t.year = yy
                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                # print(s)
                exec(s)
                t.save()
        except Exception as ex:
            pass

        llg = [1, 2, 3]
        ll = ["Scholars", "Pub", "DIndex"]

        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="EduEng")
            for k in ll:
                smm = "Res"+k
                print(smm)
                s = "mm"+k+", is_created = model_measure_dim.objects.get_or_create(measure_name='"+smm+"', measure_group_dim=gm)"
                # print(s)
                exec(s)
                if is_created:
                    s = 'mm'+k+'.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = '+smm
                    # print(s)
                    exec(s)
                    m.save()
        except Exception as ex:
            print("9029-9 Error measure:"+str(ex))

        with open(file_path) as f:
            soup = BeautifulSoup(f.read())
            try:
                rows = soup.find_all('div', {"class": "rankings-content__item"})
                n_=0
                for row in rows:
                    try:
                        # print(row)
                        n_+=1
                        # print("="*100)
                        uu = row.find("div").find("a").text.strip()
                        cc_ = row.find("span", class_= "sh").text.strip()
                        # print(uu, cc_)
                        rk_ = row.find("span", class_= "rankings-info")
                        rks_ = rk_.find_all("span", {"class": "no-wrap"})
                        llg_ = []
                        for k in rks_:
                            # print(k.text.strip())
                            llg_.append(float(k.text.replace(",", "").strip()))

                        nll = len(ll)
                        for i in range(nll):
                            # smm = "cwur" + k
                            try:
                                try:
                                    cc_ = self.check_country(cc_)
                                    c, is_created = model_country_dim.objects.get_or_create(country_name=cc_)
                                    if is_created:
                                        print("=" * 50)
                                        print(cc_)
                                        print("=" * 50)
                                        c.country_cc = cc_
                                        c.country_code = cc_
                                        c.country_name = cc_
                                        c.save()
                                except Exception as ex:
                                    print("Error country 9080-1: " + str(ex))
                                try:
                                    u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                               country_dim=c)
                                    if is_created:
                                        s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                        print(s)
                                        exec(s)
                                        u.save()
                                except Exception as ex:
                                    pass
                                try:
                                    kkk = llg_[i]
                                    # print(t, c, u, eval("mm" + ll[i]), kkk)
                                    a, is_created = model_fact.objects.get_or_create(time_dim=t, country_dim=c,
                                                                                     university_dim=u,
                                                                                     measure_dim=eval("mm" + ll[i]))
                                    a.amount = kkk
                                    a.save()
                                except Exception as ex:
                                    pass
                                # print("="*10)
                            except Exception as ex:
                                print("9085-7 Error university: " + uu + " " + str(ex))
                                continue

                    except Exception as ex:
                        pass
            except Exception as ex:
                print("Error 9070-1"+str(ex))

        # update worldBankFact
        print("="*50, "\n","move data to fact table\n", t, "\n", "="*50)
        for j in ll:
            try:
                # print("="*100, "\n", j, "\n", "="*100)
                mm = eval("mm" + j)
                qs = model_fact.objects.filter(measure_dim__measure_name=mm, time_dim=t).all()
                df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
                # print("A\n", "="*10, "\n", df)
                df = df.pivot_table(values='amount', index='country_dim_id', columns=['time_dim_id', 'measure_dim_id'],
                                aggfunc='sum')
                # print("B\n", "="*10, "\n", df)
                for k in df.columns:
                    tid = k[0]
                    mid = k[1]
                    df_ = df[k[0]][k[1]]
                    df_ = df_.reset_index()
                    # print("C\n", "=" * 10, "\n", df_)
                    for i, r in df_.iterrows():
                        # print(r)
                        cid = r["country_dim_id"]
                        if str(r[mid]) != "nan":
                            # print("=1"*50)
                            # print(r[mid])
                            amount = -1
                            try:
                                amount = r[mid]
                            except Exception as ex:
                                print("9077-77 Error "+ str(ex))
                            if amount == -1:
                                continue
                            # print(tid, type(tid), mid, type(tid), cid)
                            t = model_time_dim.objects.get(id=tid)
                            c = model_country_dim.objects.get(id=cid)
                            m=model_measure_dim.objects.get(id=mid)
                            try:
                                # print("D\n", "=" * 10, "\n", "DDDDD", yy, t, c, m)
                                f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                                # print("E\n", "=" * 10, "\n", "EEEEE", f, cr)
                                if cr:
                                    # print("F\n", "=" * 10, "\n", "FFFFFF", amount)
                                    f.amount = amount
                                    f.save()
                            except Exception as ex:
                                print("9088-88 Error "+ str(ex))

                # print("=" * 150, "\n", j, "\n", "=" * 150)
                # print("=" * 150, "\n", j, "\n", "=" * 150)
            except Exception as ex:
                print("9066-66 Error "+ str(ex))

        result = {"status": "ok"}
        return result

    def load_universitiesfile_to_db_ToBe_Deleted(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        # print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)

        # universities_file_path = os.path.join(self.target_folder, "Universities-All-v0.xlsx")
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        #
        for i, r in df.iterrows():
            try:
                cc = str(r["country"]).strip()
                c, is_created = model_country_dim.objects.get_or_create(country_name=cc)
                if is_created:
                    s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = cc'
                    exec(s)
                    c.save()
            except Exception as ex:
                # pass
                print("Error country 9080-2: "+str(r["country"])+"  -  "+str(ex))
            try:
                uu = str(r["university"]).strip()
                u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                           country_dim=c)
                if is_created:
                    s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                    exec(s)
                    u.save()
            except Exception as ex:
                # pass
                print("Error country 9080-1: "+str(r["university"])+"  -  "+str(ex))
        result = {"status": "ok"}
        return result

    def load_aifile_to_db_Old_To_Be_Deleted(self, dic):
        print("90123-6: \n", dic, "\n", "="*50)
        file_path = self.upload_file(dic)["file_path"]
        # print("file_path", file_path, "\n", "="*50)
        app_ = dic["app"]
        # print('90022-1 dic')
        dic = dic["cube_dic"]
        # print('90022-1 dic', dic, "\n", "="*50)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df.head(200))
        # #
        # print(df.columns)
        match = {"101-150":24, "151-200":22, "201-300":20, "301-400":18, "401-500":16,
                 "501-600":14, "601-700":12, "701-800":10, "801-900":8, "901-1000":6}
        for k in df.columns:
            if str(k).isnumeric():
                for z in match:
                    s= "df.loc[df["+str(k)+"] == '"+z+"', ["+str(k)+"]] ="+ str(match[z])
                    exec(s)
        # print(df.head(200))
        #
        model_name_ = dic["dimensions"]["time_dim"]["model"]
        model_time_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["country_dim"]["model"]
        model_country_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "measuregroupdim"
        model_group_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["measure_dim"]["model"]
        model_measure_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["dimensions"]["university_dim"]["model"]
        model_university_dim = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = dic["fact"]["model"]
        model_fact = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "worldbankfact"
        model_wb_fact = apps.get_model(app_label=app_, model_name=model_name_)
        #
        # Load data to UniversityFact and its dimensions.
        try:
            gm, is_created = model_group_measure_dim.objects.get_or_create(group_name="ai")
            mm = "shanghai"
            m, is_created = model_measure_dim.objects.get_or_create(measure_name=mm,
                                                                    measure_group_dim=gm)
            if is_created:
                # m.measure_code = mm
                s = 'm.' + dic["dimensions"]["measure_dim"]["field_name"] + ' = mm'
                # print(s)
                exec(s)
                m.save()
        except Exception as ex:
            print("9021-1 Error measure:"+str(ex))
        #
        for k in df.columns:
            if str(k).isnumeric():
                for index, row in df.iterrows():
                    try:
                        try:
                            cc = str(row["country"]).strip()
                            c, is_created = model_country_dim.objects.get_or_create(country_name=cc)
                            if is_created:
                                # c.country_name = cc
                                s = 'c.' + dic["dimensions"]["country_dim"]["field_name"] + ' = cc'
                                # print(s)
                                exec(s)
                                c.save()
                        except Exception as ex:
                            # pass
                            print("Error country 9080-1: "+str(ex))
                        try:
                            uu = str(row["university"]).strip()
                            u, is_created = model_university_dim.objects.get_or_create(university_name=uu,
                                                                                       country_dim=c)
                            if is_created:
                                # t.year = yy
                                s = 'u.' + dic["dimensions"]["university_dim"]["field_name"] + ' = uu'
                                # print(s)
                                exec(s)
                                u.save()
                        except Exception as ex:
                            pass
                        try:
                            yy = int(k)
                            t, is_created = model_time_dim.objects.get_or_create(id=yy)
                            if is_created:
                                # t.year = yy
                                s = 't.' + dic["dimensions"]["time_dim"]["field_name"] + ' = yy'
                                # print(s)
                                exec(s)
                                t.save()
                        except Exception as ex:
                            pass
                            # print("Error year 9080-2: "+str(ex))
                        try:
                            if str(row[k]) != "nan":
                                # print("XX1= "+str(row[k]))
                                if float("{:.2f}".format((row[k]))) > 0 or float("{:.2f}".format((row[k]))) < 0:
                                    # print(row[k], float(row[k]))
                                    # print("str:  ="+str(row[k])+"=")
                                    a, is_created = model_fact.objects.get_or_create(time_dim=t,
                                                                                     country_dim=c,
                                                                                     university_dim=u,
                                                                                     measure_dim=m)
                                    if is_created:
                                        # a.amount = float(row[k])
                                        s = 'a.' + dic["fact"]["field_name"] + ' = ' + str(
                                            float("{:.2f}".format((row[k]))))
                                        # print(s)
                                        exec(s)
                                        a.save()
                        except Exception as ex:
                            print("9026-6 Error fact: ="+str(row[k])+"="+str(ex))

                    except Exception as ex:
                        print("90666-1" + str(ex))

        # update worldBankFact
        qs = model_fact.objects.all()
        df = pd.DataFrame(list(qs.values("time_dim_id","country_dim_id","university_dim_id","measure_dim_id","amount")))
        # print(df)

        # df = df.pivot(index="time_dim_id, country_dim_id", columns='measure_dim', values='amount')

        df = df.pivot_table(values='amount', index='country_dim_id',
                            columns=['time_dim_id', 'measure_dim_id'],
                            aggfunc='sum')
        # print(df)
        for k in df.columns:
            tid = k[0]
            mid = k[1]
            df_ = df[k[0]][k[1]]
            df_ = df_.reset_index()
            # print(df_)
            for i, r in df_.iterrows():
                # print(r)
                cid = r["country_dim_id"]
                if str(r[mid]) != "nan":
                    # print("=1"*50)
                    # print(r[mid])
                    amount = r[mid]

                    # print(tid, type(tid), mid, type(tid), cid)
                    t = model_time_dim.objects.get(id=tid)
                    c = model_country_dim.objects.get(id=cid)
                    m=model_measure_dim.objects.get(id=mid)
                    f, cr = model_wb_fact.objects.get_or_create(time_dim=t ,country_dim=c, measure_dim=m)
                    if cr:
                        f.amount = amount
                        f.save()
        result = {"status": "ok"}
        return result


# class BaseDataProcessing(object):
#     def __init__(self, dic):  # to_data_path, target_field
#         self.name = 'DataProcessing'
#         # print('-'*50)
#         # print('9001 in constructor parent')
#         # print('-'*50)
#         warnings.filterwarnings(action="ignore", message="^internal gelsd")
#         # to make this notebook's output stable across runs
#
#         self.RANDOM_STATE = 42
#         np.random.seed(self.RANDOM_STATE)
#
#         # To plot pretty figures
#         mpl.rc('axes', labelsize=14)
#         mpl.rc('xtick', labelsize=12)
#         mpl.rc('ytick', labelsize=12)
#         # Where to save the figures
#         # --- Change to this when you start to use Django ---
#         self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", dic["app"])
#         # print(self.PROJECT_ROOT_DIR)
#         # print('-'*50)
#         os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)
#         self.TOPIC_ID = dic["topic_id"]  # "fundamentals"
#         self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
#         os.makedirs(self.TO_DATA_PATH, exist_ok=True)
#         self.TO_EXCEL = os.path.join(self.TO_DATA_PATH, "excel", self.TOPIC_ID)
#         os.makedirs(self.TO_EXCEL, exist_ok=True)
#         self.IMAGES_PATH = os.path.join(self.PROJECT_ROOT_DIR, "images", self.TOPIC_ID)
#         os.makedirs(self.IMAGES_PATH, exist_ok=True)
#         self.MODELS_PATH = os.path.join(self.PROJECT_ROOT_DIR, "models", self.TOPIC_ID)
#         os.makedirs(self.MODELS_PATH, exist_ok=True)
#
#         # self.TARGET_FIELD = target_field
#         # self.DATA = None
#         # self.TRAIN = None
#         # self.TEST = None
#         # self.TRAIN_TARGET = None
#         # self.TRAIN_DATA = None
#         # self.TEST_TARGET = None
#         # self.TEST_DATA = None
#         # self.train_data = None
#         # self.test_data = None
#         # self.num_attribs = None
#         # self.extra_attribs = None
#         # self.model = None
#         # self.HASH = hashlib.md5
#         # self.PIPELINE = None
#
#         # print('-'*50)
#         # print('9010 - End constructor parent')
#         # print('-'*50)
#
#     def upload_file(self, dic):
#         # print("upload_file:")
#         # print(dic)
#         # print("upload_file:")
#
#         upload_file_ = dic["request"].FILES['drive_file']
#         result = {}
#         # We can extend and add another property: data_folder
#         # like topic_id. But, we need to add this property to: params in the core view
#         # and use it here.
#         # for example: if data_folder=excel we choose self.TO_EXCEL
#
#         # print("target_folder = self.TO_"+dic["folder_type"].upper())
#         target_folder = eval("self.TO_" + dic["folder_type"].upper())
#
#         filename = dic["request"].POST['filename']
#         file_path = os.path.join(target_folder, filename)
#         with open(file_path, 'wb+') as destination:
#             for c in upload_file_.chunks():
#                 destination.write(c)
#
#         # print("9017\nUploaded\n", "-" * 30)
#         result['file_path'] = file_path
#         return result


# class DataProcessing(BaseDataProcessing):
#     def __init__(self, dic):
#         super().__init__(dic)
#
#     def get_general_data(self, dic):
#         # print("DataProcessing get_general_data 9012:\n")
#         # print(dic)
#         # print("9013:\n")
#         result = {}
#         time_dim = {}
#         country_dim = {}
#         for k in CountryDim.objects.all():
#             country_dim[k.id] = k.country_name
#
#         for k in TimeDim.objects.all():
#             time_dim[k.id] = k.year
#         result["time_dim"] = time_dim
#         result["country_dim"] = country_dim
#         return result
#
#     def load_wbfile_to_db(self, dic):
#         file_path = self.upload_file(dic)["file_path"]
#         df = pd.read_excel(file_path, sheet_name="Data", header=0)
#         # print(df)
#         n = 0
#         for k in df.columns:
#             s = k.split(" ")
#             # print("9088: ", s)
#             try:
#                 y = int(s[0])
#                 yy, is_created = TimeDim.objects.get_or_create(id=y)
#                 if is_created:
#                     yy.year = y
#                     yy.save()
#             except Exception as ex:
#                 pass
#
#         dfc = df[["Country Name", "Country Code"]]
#         # print(dfc)
#         for index, row in dfc.iterrows():
#             # print(row["Country Name"], row["Country Name"])
#             c, is_created = CountryDim.objects.get_or_create(country_code=row["Country Code"])
#             if is_created:
#                 c.country_name = row["Country Name"]
#                 c.save()
#
#         dfc = df[["Series Name", "Series Code"]]
#         # print(dfc)
#         for index, row in dfc.iterrows():
#             # print(row["Series Name"], row["Series Code"])
#             c, is_created = MeasureDim.objects.get_or_create(measure_code=row["Series Code"])
#             if is_created:
#                 c.measure_name = row["Series Name"]
#                 c.save()
#
#         # print(df)
#         for index, row in df.iterrows():
#             # print('row')
#             # print(row)
#             for k in df.columns:
#                 s = k.split(" ")
#                 try:
#                     if str(row[k]) != "nan":
#                         if float(row[k]) > 0 or float(row[k]) < 0:
#                             # print(row[k], float(row[k]))
#                             # print("str:  ="+str(row[k])+"=")
#                             y = int(s[0])
#                             t = TimeDim.objects.get(id=y)
#                             c = CountryDim.objects.get(country_code=row["Country Code"])
#                             m = MeasureDim.objects.get(measure_code=row["Series Code"])
#                             a, is_created = WorldBankFact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
#                             if is_created:
#                                 a.amount = float(row[k])
#                                 a.save()
#
#                 except Exception as ex:
#                     pass
#                     # print("90543-1" + str(ex))
#         result = {"status": "ok"}
#         return result
#
#     def load_oecdfile_to_db(self, dic):
#         # print("90123-5: \n", dic, "="*50)
#         file_path = self.upload_file(dic)["file_path"]
#         df = pd.read_excel(file_path, sheet_name="Data", header=0)
#         # print(df)
#
#         for index, row in df.iterrows():
#             try:
#                 if str(row["Value"]) != "nan":
#                     if float(row["Value"]) > 0 or float(row["Value"]) < 0:
#                         try:
#                             yy = int(row["Year"])
#                             t, is_created = TimeDim.objects.get_or_create(id=yy)
#                             if is_created:
#                                 t.year = yy
#                                 t.save()
#                         except Exception as ex:
#                             pass
#                         try:
#                             cc = row["Country"]
#                             c, is_created = CountryDim.objects.get_or_create(country_code=cc)
#                             if is_created:
#                                 c.country_name = cc
#                                 c.save()
#                         except Exception as ex:
#                             pass
#                         try:
#                             mm = row["Measurement"]
#                             print(cc, yy, mm)
#                             m, is_created = MeasureDim.objects.get_or_create(measure_name=mm)
#                             if is_created:
#                                 m.measure_code = mm
#                                 m.save()
#                         except Exception as ex:
#                             pass
#                         a, is_created = WorldBankFact.objects.get_or_create(time_dim=t, country_dim=c, measure_dim=m)
#                         if is_created:
#                             a.amount = float(row["Value"])
#                             a.save()
#             except Exception as ex:
#                 print("90652-3" + str(ex))
#
#         result = {"status": "ok"}
#         return result

