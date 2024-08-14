import warnings
import os
from django.conf import settings
import matplotlib as mpl
from bs4 import BeautifulSoup
mpl.use('Agg')
from openpyxl import Workbook, load_workbook


"""
 to_data_path_ is the place datasets are kept
 topic_id name of the chapter to store images
"""
import pandas as pd
import numpy as np
#
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from django.apps import apps


class NCESAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90044-000 NCESAlgo", dic, '\n', '-'*50)
        try:
            super(NCESAlgo, self).__init__()
        except Exception as ex:
            print("Error 90044-010 NCESDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020 CovidAlgo", dic, '\n', '-'*50)


class NCESDataProcessing(BaseDataProcessing, BasePotentialAlgo, NCESAlgo):
    def __init__(self, dic):
        super().__init__(dic)
        app_ = dic["app"]
    #     self.Debug = apps.get_model(app_label=app_, model_name="debug")
    #
    # def log_debug(self, value):
    #     self.Debug.objects.create(value=value)
    #
    # def clear_log_debug(self):
    #     self.Debug.truncate()

    def data_upload(self, dic):
        print("90121-1: \n", "="*50, "\n", dic, "\n", "="*50)

        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print(file_path)
        country_name_ = file_path.split("/")[-1].split(".")[0]
        # print(country_name_)

        sheet_name = dic["sheet_name"]
        dic = dic["cube_dic"]
        # print('90121-3 dic', dic)

        model_country_dim = apps.get_model(app_label=app_, model_name="countrydim")
        country_obj, is_created = model_country_dim.objects.get_or_create(country_name=country_name_)
        if is_created:
            country_obj.country_name = country_name_
            country_obj.save()

        model_region_dim = apps.get_model(app_label=app_, model_name="regiondim")
        model_district_dim = apps.get_model(app_label=app_, model_name="districtdim")
        model_measure_dim = apps.get_model(app_label=app_, model_name="measuredim")
        model_time_dim = apps.get_model(app_label=app_, model_name="timedim")
        model_fact = apps.get_model(app_label=app_, model_name="fact")

        wb = load_workbook(filename=file_path, read_only=False)
        ws = wb[sheet_name]
        data = ws.values
        columns_ = next(data)[0:]   # Get the first line in file as a header line
        # print("AA\n", columns_)
        columns_1 = next(data)[0:]   # Get the first line in file as a header line
        # print("BB\n", columns_1)
        # Create a DataFrame based on the second and subsequent lines of data

        columns = []
        for i in range(len(columns_)):
            f_ = columns_[i]
            f_1 = columns_1[i]
            # print(str(f_)+"_"+str(f_1))
            columns.append(str(f_)+"_"+str(f_1))
        df = pd.DataFrame(data, columns=columns)
        # df = df.reset_index()  # make sure indexes pair with number of rows
        print(df)
        #
        for i in range(len(columns)):
            if i > 1:
                f_ = columns[i]
                # print("f_ ", f_)
                yv = f_.split("_")
                year_ = yv[0]
                measure_name_ = yv[1]
                # print("HHHHHH", measure_name_, year_)

                year_obj, is_created = model_time_dim.objects.get_or_create(id=year_)
                if is_created:
                    year_obj.year = year_
                    year_obj.save()

                measure_obj, is_created = model_measure_dim.objects.get_or_create(measure_name=measure_name_)
                if is_created:
                    measure_obj.measure_name = measure_name_
                    measure_obj.save()

                for index, row in df.iterrows():
                    # print(row)
                    n_ = 0
                    region_name_ = str(row[0]).strip()
                    district_name_ = str(row[1]).strip()
                    # print("AAA ", region_name_, district_name_)
                    try:
                        region_obj, is_created = model_region_dim.objects.get_or_create(
                            country_dim=country_obj, region_name=region_name_)
                        if is_created:
                            region_obj.region_name = region_name_
                            region_obj.save()
                    except Exception as ex:
                        print("Error 90121-400-1", ex)

                    try:
                        district_obj, is_created = model_district_dim.objects.get_or_create(
                            region_dim=region_obj, district_name=district_name_)
                        if is_created:
                            district_obj.district_name = district_name_
                            district_obj.save()

                    except Exception as ex:
                        print("Error 90121-400-2", ex)

                    try:
                        v_ = float(str(row[f_]))
                        # print("ZZZZ ", f_, district_name_, v_)

                        if v_ is not None and str(v_) != "nan":
                            # print(row[columns[j]], float(str(row[columns[j]])))
                            fact_obj, is_created = model_fact.objects.get_or_create(district_dim=district_obj,
                                                                                    time_dim=year_obj,
                                                                                    measure_dim=measure_obj)
                            fact_obj.amount = v_
                            fact_obj.save()

                    except Exception as ex:
                        print("Error 90121-500", f_, district_name_, v_, "\n", ex)
        wb.close()

        result = {"status": "ok"}
        # print(result)

        return result

    def calculate_support(self, dic):
        # print(" 90121-100: \n", "=" * 50, "\n", dic, "\n", "=" * 50)
        app_ = dic["app"]
        country_id = int(dic["country_id"])
        region_id = int(dic["region_id"])
        model_fact = apps.get_model(app_label=app_, model_name="fact")

        qs = model_fact.objects.filter(district_dim__region_dim__id=region_id)

        df = pd.DataFrame(list(qs.values('time_dim_id', 'district_dim_id', 'measure_dim_id', 'amount')))

        # print(df)

        dff = pd.pivot_table(df, index=["district_dim_id"], columns=["measure_dim_id", "time_dim_id"],
                             values=["amount"], aggfunc="sum")

        dff_1 = dff.xs(1, level=1, axis=1, drop_level=False)
        dff_2 = dff.xs(2, level=1, axis=1, drop_level=False)
        # print("dff_1\n", dff_1)
        # print("dff_2\n", dff_2)

        dff_1_ = dff_1.T.reset_index()
        dff_2_ = dff_2.T.reset_index()
        dff_1_.drop(["level_0", "measure_dim_id", "time_dim_id"], axis=1, inplace=True)
        dff_2_.drop(["level_0", "measure_dim_id", "time_dim_id"], axis=1, inplace=True)
        dff_1 = dff_1_.T
        dff_2 = dff_2_.T
        # print("A21\n", dff_1)
        # print("A22\n", dff_2)

        d_ = dff_1.div(dff_2, axis=1)
        # print("d_\n", d_)
        d_["mean"] = d_.mean(axis=1)
        # print(d_["mean"])
        dd = {"district_id":[], "district_name":[], "support":[]}
        # print("dd\n", d_["mean"])
        # print(self.entities_name)

        es = self.entities_name.copy()
        es = es.set_index("id")
        dfm = pd.DataFrame(d_["mean"])
        for index, row in dfm.iterrows():
            try:
                # print(index, float(row["mean"]))
                dd["district_id"].append(index)
                dd["district_name"].append(es.loc[index].district_name)
                dd["support"].append(row["mean"])
            except Exception as ex:
                print("Error calculate_support 90-80-22", ex)
        # print(dd)
        d_["min"] = d_.min(axis=1)
        d_["max"] = d_.max(axis=1)
        d_["dev"] = d_["max"] - d_["min"]
        # print("d_2\n", d_)
        d_s = d_[["mean", "dev"]]
        # print(d_s)
        d_s_mean = d_s.mean(axis=0)
        average_national_support = d_s_mean["mean"]
        support_control_indicators = d_s_mean["dev"]

        Limits_of_Control = 0.419804464
        HLC_Value = 0.637830617

        # print(dd)
        # d = pd.DataFrame(dd)
        # print(d[:50])
        # print(d[50:100])
        # print(d[100:150])
        # print(d[150:200])
        # print(d[200:250])
        # print(d[250:300])
        # print(d[300:350])

        result = {"average_national_support":average_national_support,
                  "support_control_indicators": support_control_indicators,
                  "Limits_of_Control":Limits_of_Control,
                  "HLC_Value":HLC_Value,
                  "chart_data":dd}
        result = {"status": "ok", "result": result}
        # print(result)
        return result


