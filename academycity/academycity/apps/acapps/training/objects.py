import warnings
import os
from pathlib import Path
#
from django.conf import settings
from django.contrib.auth.models import Group
import matplotlib as mpl
mpl.use('Agg')
from ..ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from django.apps import apps
#
import pandas as pd
import numpy as np
#
import time
from datetime import timedelta, date
import shutil
#
import string
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#
from openpyxl import Workbook, load_workbook
#
from ...core.utils import log_debug, clear_log_debug

from .models import Soldiers, DoubleShoot as DoubleShootModel
from django.http import JsonResponse
import requests
from django.shortcuts import render, get_object_or_404, redirect


class TestManager(object):
    def __init__(self, dic=None):
        self.obj_dic = dic


class DoubleShoot(object):
    def __init__(self, dic=None):
        url_a = "https://qa.double-shoot.com/FlexiCore/rest/authenticationNew/login"
        a_dic = {"email": "amos@drbaranes.com", "password": "ynzVEPh9SrQf8Fgt"}
        self.authentication_key = requests.post(url_a, json=a_dic).json()["authenticationKey"]
        self.head = {'authenticationKey': '{}'.format(self.authentication_key)}
        self.url_ = "https://qa.double-shoot.com/FlexiCore/rest/plugins/Member/{}/{}"

    def get_soldier_data(self, dic=None):
        print(dic)
        ds_soldier_id = dic["ds_soldier_id"]
        function_name = dic["function_name"]
        # print("function name: ", function_name, "\nsoldier_id: ", soldier_id, "\n", "="*10)
        url_ = self.url_.format(function_name, ds_soldier_id)
        # print('\nurl_: ', url_, "\n", "="*10)
        return requests.get(url_, headers=self.head).json()

    # https://www.yellowduck.be/posts/outputting-django-queryset-json
    # print("need to get double shoot id")
    def update_or_get_soldier_data(self, dic=None):
        # print("-"*100, "\nupdate_or_get_soldier_data\n", dic, "\n", "-"*100)
        soldier_id = dic["soldier_id"]
        data = {
                'soldier_id': soldier_id,
                'double_shoot_id': "-1"
               }
        try:
            # print("90123-0 update_or_get_soldier_data 100\n", "solder_id: ", soldier_id, "\n", "-" * 100)
            soldier = Soldiers.objects.get(id=soldier_id)
            # print("90123-1 soldier obj: ", soldier)
            ds_row, is_created = DoubleShootModel.objects.get_or_create(soldier=soldier)
            data['double_shoot_id'] = ds_row.double_shoot_id
            # print(ds_row)
            # print("update_or_get_soldier_data 100-1", "\n", "-" * 100)
        except Exception as ex:
            print("90876-23: "+str(ex))
            data['double_shoot_id'] = "-100 error create record in ds model"
        # print('data 1')
        # print(data)
        # print('data 1')

        if not ds_row.is_pulled:
            try:
                # print(soldier_id)
                # print("Get data and update our system")
                function_name = dic["function_name"]
                ds_update_data = self.get_soldier_data({"ds_soldier_id": data['double_shoot_id'], "function_name": function_name})
                data["pulled_data"] = ds_update_data
                #
                # # # # update the DoubleShootModel with the pulled data.
                #
                ds_row.is_pulled = True
                ds_row.save()
            except Exception as ex:
                print("Error 9085-125 DoubleShoot update_or_get_soldier_data:\n"+ex)
                data['double_shoot_id'] = "-2"

        # update the data dictionary with data from our DoubleShootModel
        # print('data')
        # print(data)
        # print('data')

        return data


class BaseTrainingAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90050-01 BaseTrainingAlgo", dic, '\n', '-'*50)
        # super(BaseTrainingAlgo, self).__init__()
        # print("90050-02 BaseTrainingAlgo", dic, '\n', '-'*50)
        app_ = dic["app"]
        self.excel_dir = settings.MEDIA_ROOT + '/'+app_+'/excel'
        os.makedirs(self.excel_dir, exist_ok=True)
        self.save_to_file = None
        self.second_time_save = ''

    def save_to_excel(self, df, folder, file_name=None):
        if file_name:
            self.save_to_file = os.path.join(self.excel_dir, file_name)
        # print(self.save_to_file)
        try:
            # create a Path object with the path to the file
            path = Path(self.save_to_file)
            if not path.is_file():
                wb2 = Workbook()
                wb2.save(self.save_to_file)
                wb2.close()
            else:
                wb = load_workbook(filename=self.save_to_file, read_only=False)
                sheet_names = wb.sheetnames
                for f in sheet_names:
                    if f == folder:
                        wb.remove(wb[folder])
                        wb.save(self.save_to_file)
                        break
            df2 = df.copy()
            total, used, free = shutil.disk_usage("/")
        except Exception as ee:
            print("90555-52 Error objects save_to_excel: "+str(ee))
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
            # print("OK")
        except Exception as ee:
            print("90555-12 Error objects save_to_excel: "+str(ee))
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


class TrainingDataProcessing(BaseDataProcessing, BaseTrainingAlgo):
    def __init__(self, dic):
        super().__init__(dic)

        self.df_positions = pd.DataFrame.from_dict({"id" :[1,2,3,4,5,0],
                                          "position_name": ["Captain","Officer","Soldier","Colonel","Sous Officer","Other"]})

        self.df_instructor_positions = pd.DataFrame.from_dict({"id" :[1,2,3,4,5,6,7,8],
                                          "position_name": ['מפקד גדוד', 'מפקד פלוגה', 'מספר 2 – צ', 'מוביל צוות', 'מספר 2',
                                                            'אימון גופני', 'מתגבר', 'קמ”ג']})

    # To be deleted
    def process_period_1(self, app_, n, nav_tables_, result, qid=None, battalion=None):
        nn = len(nav_tables_)
        if n < nn:
            model_ = apps.get_model(app_label=app_, model_name=nav_tables_[n]+"s")
            p_key_field_name = model_._meta.pk.name
            if qid:
                model_name = nav_tables_[n-1]
                model_p = apps.get_model(app_label=app_, model_name=model_name+"s").objects.get(id=qid)
                qs = eval("model_.objects.filter("+model_name+"=model_p).all()")
            else:
                qs = model_.objects.filter(id=battalion).all()
            n += 1
            if nav_tables_[n-1] == "soldier":
                model_periods = apps.get_model(app_label=app_, model_name="periods")
                period_obj, is_created = model_periods.objects.get_or_create(battalion__id=battalion, period_number=1)
                model_soldiers = apps.get_model(app_label=app_, model_name="soldiers")
                model_unit_soldiers = apps.get_model(app_label=app_, model_name="unitsoldiers")
                df = pd.DataFrame(list(qs.values('user_id', 'platoon_id')))
                # print(df)
                for index, row in df.iterrows():
                    soldier_obj = model_soldiers.objects.get(user_id=row["user_id"])
                    u_obj, is_created = model_unit_soldiers.objects.get_or_create(period=period_obj, soldier=soldier_obj)
                    u_obj.unit_number = row["platoon_id"]
                    u_obj.save()
                return result
            for q in qs:
                if p_key_field_name=="user":
                    qid_ = eval("q."+p_key_field_name+".id")
                else:
                    qid_ = eval("q."+p_key_field_name)
                if n < nn-1:
                    n_ = self.get_next_number({"app": app_})
                else:
                    n_ = qid_
                result[n_]={"title":str(q), "data":{}}
                self.process_period_1(app_, n, nav_tables_, result[n_]["data"], qid=qid_, battalion=battalion)
        return result

    # To be deleted
    def get_units_structure_battallion_1_Period_1(self, dic):
        # print("\n", "-"*50, '\n90035-1 dic\n', dic, "\n", "-"*50)
        app_ = dic["app"]
        battalion_ = dic["battalion"]
        period_ = dic["period"]
        #
        groups_ = dic["groups"]
        nav_tables_ = groups_["nav_tables"]
        result = {"title":"title-top", "data":{}}

        result = self.process_period_1(app_, 0, nav_tables_, result["data"], battalion=battalion_)
        model_periods = apps.get_model(app_label=app_, model_name="periods")
        period_obj, is_created = model_periods.objects.get_or_create(battalion__id=battalion_, period_number=period_)
        period_obj.structure = result
        period_obj.period_name = "Battalion: " + str(battalion_) +" Period: " + str(period_)
        period_obj.save()

        # print("-"*100, "\n", result, "\n", "-"*100)
        result = {"status": "ok", "result":result}
        return result

    def process_weeks_1_5(self, app_, n, nav_tables_, result, qid=None, battalion=None):
        nn = len(nav_tables_)
        if n < nn:
            title = nav_tables_[n]
            # print(title)
            # result[nav_tables_[n]]={}
            model_ = apps.get_model(app_label=app_, model_name=nav_tables_[n]+"s")
            p_key_field_name = model_._meta.pk.name
            if qid:
                model_name = nav_tables_[n-1]
                # print(title, p_key_field_name, model_name)
                model_p = apps.get_model(app_label=app_, model_name=model_name+"s").objects.get(id=qid)
                qs = eval("model_.objects.filter("+model_name+"=model_p).all()")
            else:
                qs = model_.objects.filter(id=battalion).all()
            n += 1
            for q in qs:
                if p_key_field_name=="user":
                    qid_ = eval("q."+p_key_field_name+".id")
                    # print("q." + p_key_field_name, model_, qid_, q.userid)
                else:
                    qid_ = eval("q."+p_key_field_name)
                result[qid_]={"title":str(q), "model":nav_tables_[n-1], "data":{}}
                self.process_weeks_1_5(app_, n, nav_tables_, result[qid_]["data"], qid=qid_, battalion=battalion)
        return result

    def process_weeks_6_10(self, app_, weeks, weeks_dic, result, qid=None):
        model_ = apps.get_model(app_label=app_, model_name="unitesoldiers")
        objs = model_.objects.filter(weeks = weeks).all()

        print(weeks_dic)

        return weeks_dic

    def get_units_structure(self, dic):
        # print("\n", "-"*50, '\n90035-1 dic\n', dic, "\n", "-"*50)
        app_ = dic["app"]
        weeks_ = dic["weeks"]
        battalion_ = dic["battalion"]
        #
        groups_ = dic["groups"]
        nav_tables_ = groups_["nav_tables"]
        result = {"title":"title-top", "data":{}}
        if weeks_ == "1-5":
            result = self.process_weeks_1_5(app_, 0, nav_tables_, result["data"], battalion=battalion_)

        # print("-"*100, "\n", result, "\n", "-"*100)
        result = {"status": "ok", "result":result}
        return result

    def get_units_structure_new(self, dic):
        print("\n", "-"*50, '\n90035-1 dic\n', dic, "\n", "-"*50)
        app_ = dic["app"]
        battalion_ = dic["battalion"]
        # soldiers
        try:
            soldiers = {"id":[], "userid":[], "first_name":[], "last_name":[], "name":[]}
            model_soldiers = apps.get_model(app_label=app_, model_name="soldiers")
            qs = model_soldiers.objects.filter(battalion__id=battalion_).all()
            # print(qs)
            df_s = pd.DataFrame(list(qs.values("user_id", "userid", "first_name", "last_name")))
            # print(df_s)
            for index, row in df_s.iterrows():
                soldiers["id"].append(str(row["user_id"]))
                soldiers["userid"].append(str(row["userid"]))
                soldiers["first_name"].append(str(row["first_name"]))
                soldiers["last_name"].append(str(row["last_name"]))
                soldiers["name"].append(str(row["first_name"])+" "+str(row["last_name"]))
        except Exception as ex:
            print("Error 1: "+str(ex))

        # unitsoldiers
        try:
            unitsoldiers = {}
            model_unitsoldiers = apps.get_model(app_label=app_, model_name="unitsoldiers")
            qs = model_unitsoldiers.objects.filter(period__battalion__id=battalion_).all()
            df_us = pd.DataFrame(list(qs.values()))
            # print(df_us)
            period_id_ = []
            unit_number_ = []
            for index, row in df_us.iterrows():
                if row["period_id"] not in period_id_:
                    unitsoldiers[int(row["period_id"])] = {}
                    period_id_.append(row["period_id"])
                if row["unit_number"] not in unit_number_:
                    unitsoldiers[int(row["period_id"])][int(row["unit_number"])] = []
                    unit_number_.append(row["unit_number"])
                unitsoldiers[int(row["period_id"])][int(row["unit_number"])].append(int(row["soldier_id"]))
            # print(unitsoldiers)
        except Exception as ex:
            print("Error 2: "+str(ex))

        # structure periods
        try:
            structure = {}
            period = {}
            model_periods = apps.get_model(app_label=app_, model_name="periods")
            period_objs = model_periods.objects.filter(battalion__id=battalion_).all()
            # print(period_objs)
            for period_obj in period_objs:
                structure[period_obj.id] = period_obj.structure
                period[period_obj.id] = {"n_limit": period_obj.n_limit}
        except Exception as ex:
            print("Error 3: "+str(ex))
        print("-"*100, "\n", structure, "\n", "-"*100)
        result = {"status": "ok", "soldiers": soldiers, "structure":structure, "unitsoldiers":unitsoldiers,
                  "period":period}
        # print(result)
        return result

    def set_instructors(self, dic):
        # print('90088-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print("-"*100, "\n", file_path, "\n", "-"*100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        # print("-"*100)
        model_instructors = apps.get_model(app_label=app_, model_name="instructors")
        model_companys = apps.get_model(app_label=app_, model_name="companys")
        model_platoons = apps.get_model(app_label=app_, model_name="platoons")
        model_battalions = apps.get_model(app_label=app_, model_name="battalions")
        my_group, is_created = Group.objects.get_or_create(name='t_simple_user')

        try:
            u = User.objects.get(first_name="admin", last_name="admin")
            print(u)
            instructor_obj, is_created = model_instructors.objects.get_or_create(user=u)
            instructor_obj.first_name = "admin"
            instructor_obj.last_name = "admin"
            # instructor_obj.position = 0
            instructor_obj.save()
        except Exception as ex:
            print("9001-01 Error " + str(ex))

        for index, row in df.iterrows():
            company_name_ = str(row["company_name"]).upper()
            first_name_ = str(row["first_name"])
            last_name_ = str(row["last_name"])
            username_ = str(row["username"])
            password_ = str(row["password"])
            position_name_ = str(row["position_name"])
            position_ = int(self.df_instructor_positions[self.df_instructor_positions["position_name"]==position_name_]["id"])
            # print("9088-1", company_name_, first_name_, " ", last_name_, position_name_)

            try:
                u = User.objects.get(username=username_)
                count = u.delete()
                # print("B count\n", count, "\n")
            except Exception as ex:
                # pass
                print("9055-55 Error " + str(ex))
            try:
                u = User.objects.create_user(username=username_, email=username_+'@gmail.com',
                                             password=password_)
                # print(u.password)
                u.first_name = first_name_
                u.last_name = last_name_
                u.save()
                my_group.user_set.add(u)
                my_group.save()
            except Exception as ex:
                print("9000-00 Error " + str(ex))
            try:
                instructor_obj, is_created = model_instructors.objects.get_or_create(user=u)
                instructor_obj.first_name = first_name_
                instructor_obj.last_name = last_name_
                instructor_obj.position = position_
                instructor_obj.save()
            except Exception as ex:
                print("9001-01 Error " + str(ex))

            print("Record 9088-3   ", company_name_, instructor_obj, "  =", is_created)

            try:
                if company_name_ != "Battalion".upper():
                    # print(company_name_)
                    company_obj = model_companys.objects.get(company_name=company_name_)
                    if str(row["platoon_number"]).lower() != "nan":
                        platoon_number = float(str(row["platoon_number"]))
                        platoon_obj = model_platoons.objects.get(platoon_number=platoon_number, company=company_obj)
                        platoon_obj.instructor.add(instructor_obj)
                        if position_ == 2:
                            company_obj.instructor.add(instructor_obj)
                        platoon_obj.save()
                    else:
                        # print("no platoon")
                        company_obj.instructor.add(instructor_obj)
                        company_obj.save()
                else:
                    try:
                        battalion_obj, is_created = model_battalions.objects.get_or_create(battalion_number=1)
                    except Exception as ex:
                        print("9011-1111 Error " + str(ex))
                    try:
                        battalion_obj.instructor.add(instructor_obj)
                    except Exception as ex:
                        print("9011-1122 Error " + str(ex))
                    try:
                        battalion_obj.save()
                    except Exception as ex:
                        print("9011-1133 Error " + str(ex))
            except Exception as ex:
                print("9022-22 Error " + str(ex))

        print("Done")
        result = {"status": "ok"}
        return result

    def set_soldiers(self, dic):
        # print('90022-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print("-"*100, "\n", file_path, "\n", "-"*100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        # print(df)
        # print("-"*100)

        model_name_ = "instructors"
        model_instructors = apps.get_model(app_label=app_, model_name=model_name_)

        try:
            u = User.objects.get(username="dinstructor")
            count = u.delete()
            # print("B count\n", count, "\n")
        except Exception as ex:
            pass
            # print("9055-55 Error " + str(ex))

        my_group, is_created = Group.objects.get_or_create(name='t_simple_user')
        try:
            u = User.objects.create_user(username="dinstructor", email='dinstructor@gmail.com', password='DINSTRUCTOR123#')
            # print(u.password)
            u.first_name = "dinstructor"
            u.last_name = "dinstructor"
            u.save()
            # print(u)
            my_group.user_set.add(u)
            my_group.save()
        except Exception as ex:
            print("9000-00 Error " + str(ex))

        try:
            instructor_obj, is_created = model_instructors.objects.get_or_create(first_name='default_instructor1',
                                                                                 user=u)
        except Exception as ex:
            print("9001-01 Error " + str(ex))
        # print("-"*100, "\n", instructor_obj, "  =", is_created, "\n", "-"*100)

        model_name_ = "brigades"
        model_brigades = apps.get_model(app_label=app_, model_name=model_name_)
        brigade_obj, is_created = model_brigades.objects.get_or_create(brigade_name='brigade 1')
        # print("-"*100, "\n", brigade_obj, "  =", is_created, "\n", "-"*100)

        model_name_ = "battalions"
        model_battalions = apps.get_model(app_label=app_, model_name=model_name_)
        battalion_obj, is_created = model_battalions.objects.get_or_create(battalion_name='battalion 1', brigade=brigade_obj)
        battalion_obj.instructor.add(instructor_obj)
        battalion_obj.save()
        # print("-"*100, "\n", battalion_obj, "  ", is_created, "\n", "-"*100)

        model_name_ = "courses"
        model_courses = apps.get_model(app_label=app_, model_name=model_name_)
        course_obj, is_created = model_courses.objects.get_or_create(course_name='course 1')
        course_obj.instructor.add(instructor_obj)

        model_name_ = "companys"
        model_companys = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "platoons"
        model_platoons = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "squads"
        model_squads = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "soldiers"
        model_soldier = apps.get_model(app_label=app_, model_name=model_name_)

        # model_user = get_user_model()
        ll = []
        ll_ = []
        ll1 = []
        ll1_ = []
        llf = []
        llf_ = []
        llfn = []
        llfn_ = []
        n__ = 0
        for index, row in df.iterrows():
            if n__ > 10000:
                break
            n__ += 1
            # print(row, "\n", row["COMPANY"])
            company_name_ = str(row["COMPANY"]).upper()
            company_number = int(row["COMPANYID"])
            username_ = str(23*10000+company_number*1000+int(row["SN"]))
            company_obj, is_created = model_companys.objects.get_or_create(company_name=company_name_, battalion=battalion_obj)
            if is_created:
                # print("-"*100, "\n", company_obj, "  ", is_created, "\n", "-"*100)
                company_obj.company_number = company_number
                company_obj.instructor.add(instructor_obj)
                company_obj.save()
            # str(int(row["PLATOON"]))
            platoon_name_n = int(row["PLATOON"])
            platoon_name_ = company_name_ + " " +str(platoon_name_n)
            platoon_obj, is_created = model_platoons.objects.get_or_create(platoon_name=platoon_name_, company=company_obj)
            if is_created:
                platoon_obj.platoon_number = platoon_name_n
                platoon_obj.instructor.add(instructor_obj)
                platoon_obj.save()
                # print("-"*100, "\n", platoon_obj, "  ", is_created, "\n", "-"*100)

            squad_name_ = '1'
            squad_obj, is_created = model_squads.objects.get_or_create(squad_name=squad_name_, platoon=platoon_obj)
            squad_obj.save()
            # print("-"*100, "\n", squad_obj, "  ", is_created, "\n", "-"*100)
            full_name = string.capwords(str(row["FULLNAME"]))
            nn__ = full_name.find(" ")
            first_name = full_name[:nn__]
            last_name = full_name[nn__+1:]
            mz4psn = str(row["MZ4PSN"])
            ramonsn = str(row["RAMONSN"])
            shoes_size = float(row["shoes_size"])
            uniform_size = str(row["uniform_size"])
            sport_size = str(row["sport_size"])
            if mz4psn not in ll:
                ll.append(mz4psn)
            else:
                ll_.append(mz4psn)
                print("mz4psn= ", mz4psn)
            if ramonsn not in ll1:
                ll1.append(ramonsn)
            else:
                ll1_.append(ramonsn)
                print("ramonsn= ", ramonsn)

            # if first_name not in llf:
            #     llf.append(first_name)
            # else:
            #     llf_.append(first_name)
            #     print("first_name= ", first_name)
            # if full_name not in llfn:
            #     llfn.append(full_name)
            # else:
            #     llfn_.append(full_name)
            #     print("full_namen= ", full_name)

            position = str(row["POSITION"]).upper()

            if position == "NAN":
                position = ""
            #  "A \n", "-"*100, "\n",
            print("full name", full_name, " first name=", first_name,"username_",username_,
                  " last name=", last_name, " position=", position,
                  " mz4psn", mz4psn, " ramonsn=", ramonsn,
                  shoes_size, uniform_size, sport_size)

            try:
                u = User.objects.get(username=username_)
                count = u.delete()
                # print("B count\n", count, "\n")
            except Exception as ex:
                pass
                # print("9055-55 Error " + str(ex))

            try:
                u = User.objects.create_user(username=username_, email=username_+'@gmail.com', password=company_name_+username_+'#')
                # print(u.password)
                u.first_name = first_name
                u.last_name = last_name
                u.save()
                # print(u)
                my_group.user_set.add(u)
                my_group.save()
            except Exception as ex:
                print("9011-11 Error " + str(ex))

            try:
                soldier, is_created = model_soldier.objects.get_or_create(user=u, platoon=platoon_obj)
                soldier.first_name = first_name
                soldier.last_name = last_name
                soldier.userid = username_
                try:
                    p_ = position.lower().strip()
                    if p_ == "":
                        p_ = "Other"
                    elif p_ == "officier":
                        p_ = "Officer"
                    elif p_ == "soldeir":
                        p_ = "Soldier"
                    elif p_ == "sous officier":
                        p_ = "Sous Officer"
                    else:
                        p_ = p_.title()
                    position = int(self.df_positions[self.df_positions["position_name"]==p_]["id"])
                except Exception as ex:
                    print("90888-66 Training objects set_soldiers Error: " + p_ +str(ex))
                soldier.position = position
                soldier.mz4psn = mz4psn
                soldier.ramonsn = ramonsn
                #
                soldier.shoes_size = shoes_size
                soldier.uniform_size = uniform_size
                soldier.sport_size = sport_size
                soldier.save()
                course_obj.course_soldiers.add(soldier)
                course_obj.save()
            except Exception as ex:
                print("9033-53 Error " + str(ex))

        # print(llf, "\n\n", llf_)
        # print("1="*10, "\n\n")
        # print(llfn, "\n\n", llfn_)
        # print("2="*10, "\n\n")
        #
        print(ll, "\n\n", ll1)
        print("="*100, "\n\n")
        print(ll_, "\n\n", ll1_)
        print("="*100, "\n\n")
        #
        # ukkk = authenticate(username='testsold', password='Amos122#')
        # print(ukkk)
        # print(ukkk.email)
        # try:
        #     print(u.user_training)
        # except Exception as ex:
        #     print("9044-54 Error " + str(ex))

        # print("-"*100, "\n", my_group, "  ", is_created, "\n", "-"*100)
        # print('90022-3 dic')

        # my_group.user_set.add(your_user)

        result = {"status": "ok"}
        return result

    def update_soldiers(self, dic):
        print('90033-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        print("-" * 100, "\n", file_path, "\n", "-" * 100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)
        print("-" * 100)

        # model_name_ = "companys"
        # model_companys = apps.get_model(app_label=app_, model_name=model_name_)
        # model_name_ = "platoons"
        # model_platoons = apps.get_model(app_label=app_, model_name=model_name_)
        # model_name_ = "soldiers"
        # model_soldier = apps.get_model(app_label=app_, model_name=model_name_)
        # for index, row in df.iterrows():
        #     soldier_obj = model_soldier.objects.get(ramonsn=str(row["RAMONSN"]))
        #     soldier_obj.mz4psn = str(row["MZ4PSN"])
        #     platoon_obj = model_platoons.objects.get(company__company_name=str(row["COMPANY"]),
        #                                                  platoon_name=str(row["PLATOON"]))
        #     soldier_obj.platoon = platoon_obj
        #
        #     soldier_obj.save()

        result = {"status": "ok"}
        return result

    def delete_soldiers(self, dic):
        print('90044-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        print("-" * 100, "\n", file_path, "\n", "-" * 100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)
        print("-" * 100)

        result = {"status": "ok"}
        return result

    def de_activate_soldiers(self, dic):
        print('90044-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        print("-" * 100, "\n", file_path, "\n", "-" * 100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)
        print("-" * 100)

        result = {"status": "ok"}
        return result

    def create_dates_in_time_dim(self, dic):
        # print('90099-1 dic', dic)
        app_ = dic["app"]
        model_name = dic["model_name"]
        model_ = apps.get_model(app_label=app_, model_name=model_name)
        start_date = date.today() + timedelta(days=-90) # Monday = 0
        for i in range(1000):
            t = start_date + timedelta(days=i)
            y = t.year
            m = t.month
            d = t.day
            id_ = y * 10000 + m * 100 + d
            # print(y, m, d, id_)
            obj, is_create = model_.objects.get_or_create(id=id_)
            obj.year = y
            obj.month = m
            obj.day = d
            obj.save()
        result = {"status": "ok"}
        return result

    def daily_run(self, dic):
        print(dic)
        app_ = dic["app"]
        model_name_ = "soldiers"
        model_soldier = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "platoons"
        model_platoon = apps.get_model(app_label=app_, model_name=model_name_)

        qs = model_platoon.objects.all()
        df_p = pd.DataFrame(list(qs.values("id", "platoon_name")))
        qs = model_soldier.objects.all()
        df = pd.DataFrame(list(qs.values("platoon_id","is_confirmed","first_name","last_name","image",
                                         "userid","mz4psn","ramonsn","address","city","state","zip","country",
                                         "email","phone","birthday","num_of_children","marital_status",
                                         "shoes_size", "uniform_size", "sport_size", "uniform_size","height","weight","blood_type","position","rank",
                                         "profession","sub_profession","medical_condition")))

        dfm = df.merge(df_p, left_on='platoon_id', right_on='id')
        dfm = dfm.drop(["platoon_id", "id"], axis=1)
        # print(dfm.iloc[0])
        # print("="*20)
        dfm = dfm.merge(self.df_positions, left_on='position', right_on='id')
        dfm = dfm.drop(["position", "id"], axis=1)

        # print(dfm.iloc[0])
        # print("="*20)
        self.save_to_excel(dfm, "SoldiersList", file_name="daily_run.xlsx")

        result = {"status": "ok"}
        return result

    def excel_gun_list(self, dic):
        print('90033-100 dic\n', '-'*100, '\n', dic, '\n', '-'*100)
        app_ = dic["app"]
        model_name_ = "soldiers"
        model_soldier = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "inventorys"
        model_inventorys = apps.get_model(app_label=app_, model_name=model_name_)
        model_name_ = "inventorycategorys"
        model_inventorycategorys = apps.get_model(app_label=app_, model_name=model_name_)

        qs = model_inventorys.objects.all()
        df_i = pd.DataFrame(list(qs.values('id', 'inventorycategory_id', 'inventory_number')))
        qs = model_inventorycategorys.objects.all()
        df_ic = pd.DataFrame(list(qs.values('id', 'category_name')))
        dfm = df_i.merge(df_ic, left_on='inventorycategory_id', right_on='id')
        dfm = dfm.drop(["inventorycategory_id", 'id_y'], axis=1)
        dfm.columns = ['id', 'inventory_number', 'category_name']

        qs = model_soldier.objects.all()
        df_s = pd.DataFrame(list(qs.values('user_id', 'userid', 'first_name', 'last_name', 'gun_mz4psn_id', 'gun_ramonsn_id')))
        df_s['userid'] = df_s['userid'] + ":" + df_s['first_name'] + " " + df_s['last_name']
        df_s = df_s.drop(['first_name', 'last_name'], axis=1)
        dfm = df_s.merge(dfm, how='outer', left_on='gun_mz4psn_id', right_on='id')
        #
        dfm = df_s.merge(dfm, how='outer', left_on='gun_ramonsn_id', right_on='id')
        #
        dfm = dfm.drop(['id', 'gun_mz4psn_id_x', 'gun_mz4psn_id_y', 'gun_ramonsn_id_x', 'gun_ramonsn_id_y'], axis=1)
        dfm['userid'] = dfm.apply(lambda row: row["userid_y"] if np.isnan(row["user_id_x"]) else row["userid_x"], axis=1)
        dfm = dfm.drop(['user_id_x', 'user_id_y', 'userid_x', 'userid_y'], axis=1)
        # print(dfm)
        # print("5="*20)
        df = dfm.pivot_table(values='inventory_number', index='userid', columns=['category_name']
                             , aggfunc='sum'
                             )
        print(df)
        self.save_to_excel(df, "GunsList", file_name="guns_list.xlsx")

        result = {"status": "ok"}
        return result

    def set_guns(self, dic):
        print('90088-1 dic', dic)
        app_ = dic["app"]
        file_path = self.upload_file(dic)["file_path"]
        # print("-"*100, "\n", file_path, "\n", "-"*100)
        df = pd.read_excel(file_path, sheet_name="Data", header=0)
        print(df)
        print("-"*100)
        model_inventorys = apps.get_model(app_label=app_, model_name="inventorys")
        model_inventorycategorys = apps.get_model(app_label=app_, model_name="inventorycategorys")
        columns = df.columns
        print(columns)
        for c in columns:
            print(c)
            inventory_category_obj, is_create = model_inventorycategorys.objects.get_or_create(category_name=c)
            inventory_category_obj.save()
            for index, row in df.iterrows():
                gun_number = str(row[c]).upper()
                print(gun_number)
                inventory_obj, is_created = model_inventorys.objects.get_or_create(inventorycategory=inventory_category_obj,
                                                                                   inventory_number=gun_number)
                inventory_obj.save()
        print("-"*50, "\n\nDone")

        result = {"status": "ok"}
        return result

    def set_new_structure(self, dic):
        print('90088-1 dic', dic)
        app_ = dic["app"]
        battalion_name = dic["cube_dic"]["fact"]["model"]
        battalion_id = int(dic["cube_dic"]["fact"]["field_name"])
        period_number = int(dic["cube_dic"]["dimensions"]["time_dim"]["field_name"])

        units_dic = {battalion_id: {'title': battalion_name, 'data': {}}}
        file_path = self.upload_file(dic)["file_path"]
        sheet_name_ = eval(dic["sheet_name"])
        model_periods = apps.get_model(app_label=app_, model_name="periods")
        period_obj, is_created = model_periods.objects.get_or_create(battalion__id=battalion_id, period_number=period_number)
        model_unit_soldiers = apps.get_model(app_label=app_, model_name="unitsoldiers")
        model_unit_soldiers.truncate()
        model_soldiers = apps.get_model(app_label=app_, model_name="soldiers")
        missing_soldiers = []
        multiple_soldiers = []
        for sheet in sheet_name_:
            number = self.get_next_number({"app": app_})
            # company
            units_dic[battalion_id]["data"][number] = {"title": sheet, "data": {}}
            data_ = units_dic[battalion_id]["data"][number]["data"]
            df = pd.read_excel(file_path, sheet_name=sheet, header=0)
            # print(df)
            platoons_ = []
            n__ = 0
            for index, row in df.iterrows():
                n__+= 1
                # print("=====", n__, "=====")
                platoon = str(row["Unit"])
                if platoon not in platoons_:
                    # platoon
                    platoons_.append(platoon)
                    number_ = self.get_next_number({"app": app_})
                    data_[number_] = {"title": platoon, "data": {}}
                    sections_ = []
                section = str(row["Sub"])
                if section not in sections_:
                    sections_.append(section)
                    # print(platoon, section)
                    # print(platoons_, sections_)
                    number__ = self.get_next_number({"app": app_})
                    data_[number_]["data"][number__] = {"title": section, "data": {}}

                full_name = string.capwords(str(row["FULLNAME"]))
                if full_name == "Nan":
                    continue
                nn__ = full_name.find(" ")
                first_name = full_name[:nn__].rstrip().lstrip()
                last_name = full_name[nn__+1:].rstrip().lstrip()

                try:
                    soldier_obj = model_soldiers.objects.filter(first_name=first_name).all()
                    count = soldier_obj.count()
                    if count == 0:
                        soldier_obj = model_soldiers.objects.filter(last_name=last_name).all()
                        count = soldier_obj.count()
                        if count == 0:
                            missing_soldiers.append(platoon+": " + section + ": " + full_name)
                            print(n__, " AAA (count == 0)=", platoon+": " + section + ": " + full_name)
                            continue
                    elif count > 1:
                        soldier_obj = model_soldiers.objects.filter(first_name=first_name, last_name=last_name).all()
                        count = soldier_obj.count()
                        if count > 1:
                            multiple_soldiers.append("2 "+full_name)
                            print(n__, "BBB(count >1)=", platoon+": " + section + ": " + full_name)
                            continue
                        elif count == 0:
                            print(n__, "DDD (count == 1 w LN count=0)=", platoon+": " + section + ": " + full_name)
                            multiple_soldiers.append("2 "+full_name)
                            continue
                    if soldier_obj.count() == 1:
                        try:
                            u_obj, is_created = model_unit_soldiers.objects.get_or_create(period=period_obj, soldier=soldier_obj[0])
                            u_obj.unit_number = number__
                            u_obj.save()
                            # print("saved: "+ str(n__))
                        except Exception as ex:
                            print("error 200: ", full_name)
                    else:
                        print(str(n__)+" HHH Not saved: (count="+str(soldier_obj.count())+")= ", platoon+": " + section + ": " + full_name)
                except Exception as ex:
                    print("Missin soldier in DB: platoon=" + platoon + ": section=" + section + ": first_name=" + first_name + "= last_name=" + last_name + "=\n" + str(ex))
                    # missing_soldiers.append(full_name)

        period_obj.structure = units_dic
        period_obj.period_name = "Battalion: " + str(battalion_id) + " Period: " + str(period_number)
        period_obj.save()
        print('\n missing_soldiers')
        print(missing_soldiers)
        print('\n multiple_soldiers')
        print(multiple_soldiers)
        print(units_dic)

        print("-"*50, "\n\nDone")

    def update_gun_list(self, dic):
        print('900100-1 dic', dic)
        clear_log_debug()
        app_ = dic["app"]
        model_soldiers = apps.get_model(app_label=app_, model_name="soldiers")
        model_inventorys = apps.get_model(app_label=app_, model_name="inventorys")
        qs = model_soldiers.objects.all()
        for q in qs:
            try:
                print(q.mz4psn)
                log_debug(str(q.mz4psn))
                im_obj = model_inventorys.objects.get(inventory_number=q.mz4psn)
            except Exception as ex:
                log_debug("9095-100 Error updating guns: get q.mz4psn " + str(q.mz4psn))

            try:
                q.gun_mz4psn = im_obj
                q.save()
            except Exception as ex:
                # pass
                log_debug("9095-100 Error updating guns: set 1 and save " + str(q.mz4psn))

            try:
                ir_obj = model_inventorys.objects.get(inventory_number=q.ramonsn)
            except Exception as ex:
                log_debug("9095-100 Error updating guns: get ramonsn" + " " + str(q.ramonsn))

            try:
                q.gun_ramonsn = ir_obj
                q.save()
            except Exception as ex:
                log_debug("9095-100 Error updating guns: save ramonsn"  + " " + str(q.ramonsn))

        result = {"status": "ok"}
        return result

    def get_variable_data(self, dic):
        print('90065-11 dic', dic, "\n", "-"*50)
        app_ = dic["app"]
        record_id = dic["tests_dic"]["record_id"]
        group_list = dic["group_dic"]
        #
        parent_test_table = dic["tests_dic"]["parent_table"]
        parent_test_model_ = apps.get_model(app_label=app_, model_name=parent_test_table)
        parent_test_obj = parent_test_model_.objects.get(id=record_id)
        test_table = dic["tests_dic"]["table"]
        test_model_ = apps.get_model(app_label=app_, model_name=test_table)
        #
        tests_objs = test_model_.objects.filter(testsvariable=parent_test_obj).all()
        # print(tests_objs)
        test_list = []
        test_dic = {}
        up_value = parent_test_obj.up_value
        up_color = parent_test_obj.up_color
        down_value = parent_test_obj.down_value
        down_color = parent_test_obj.down_color
        other_color = parent_test_obj.other_color
        var_dic = {"up_value":up_value, "up_color":up_color, "down_value":down_value,
                   "down_color":down_color, "other_color":other_color}
        for q in tests_objs:
            test_list.append(str(q.test_number))
            test_dic[str(q.test_number)] = {"id": q.id , "value": round(float(q.value),2)}
        # print('test_dic')
        # print(test_dic)

        grades_model_ = apps.get_model(app_label=app_, model_name="gradesforevents")
        q_gs = grades_model_.objects.filter(soldiersforevent__soldier_number__in=group_list,
                                            testsforevent__test_number__in=test_list).order_by("soldiersforevent__soldier_number",
                                                                                               "testevent__id").all()

        result={"soldier_number":[], "event_id":[], "event_date":[], "test_number":[], "value":[]}
        for q in q_gs:
            # print(q.testevent.test_event_name)
            # print(q.testevent.id)
            result["event_id"].append(q.testevent.id)
            result["event_date"].append(q.testevent.time_dim.id)
            result["soldier_number"].append(q.soldiersforevent.soldier_number)
            result["test_number"].append(q.testsforevent.test_number)
            result["value"].append(round(float(q.value),2))
        result = {"status": "ok", "result":result, "test_dic":test_dic, "var_dic": var_dic}
        # print(result)
        return result

    # def get_periods_of_battalion(self, dic):
    #     # print('90065-11 dic', dic)
    #     app_ = dic["app"]
    #     battalion_id = int(dic["battalion_id"])
    #     periods_model_ = apps.get_model(app_label=app_, model_name="periods")
    #     period_objs = periods_model_.objects.filter(battalion__id=battalion_id).all()
    #
    #     periods = []
    #     test_dic = {}
    #     up_value = parent_test_obj.up_value
    #     up_color = parent_test_obj.up_color
    #     down_value = parent_test_obj.down_value
    #     down_color = parent_test_obj.down_color
    #     other_color = parent_test_obj.other_color
    #     var_dic = {"up_value":up_value, "up_color":up_color, "down_value":down_value,
    #                "down_color":down_color, "other_color":other_color}
    #     for q in tests_objs:
    #         test_list.append(str(q.test_number))
    #         test_dic[str(q.test_number)] = {"id": q.id , "value": round(float(q.value),2)}
    #     # print('test_dic')
    #     # print(test_dic)
    #
    #     grades_model_ = apps.get_model(app_label=app_, model_name="gradesforevents")
    #     q_gs = grades_model_.objects.filter(soldiersforevent__soldier_number__in=group_list,
    #                                         testsforevent__test_number__in=test_list).order_by("soldiersforevent__soldier_number").all()
    #     result={"soldier_number":[], "test_number":[], "value":[]}
    #     for q in q_gs:
    #         result["soldier_number"].append(q.soldiersforevent.soldier_number)
    #         result["test_number"].append(q.testsforevent.test_number)
    #         result["value"].append(round(float(q.value),2))
    #
    #     result = {"status": "ok", "result":result, "test_dic":test_dic, "var_dic": var_dic}
    #     # print(result)
    #     return result

# double_shoot = DoubleShoot()
# # function = "getSolderData"
# dic = {"function_name": "getMember", "soldier_id": "RoxASKgvRGaR90ZuAnc3Gw"}
# r = double_shoot.get_soldier_data(dic)

