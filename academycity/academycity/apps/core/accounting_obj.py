from django.shortcuts import get_object_or_404
from ..courses.models import GeneralLedger, ChartOfAccounts
from .utils import get_number, add_years_months_days
from .sql import SQL
from datetime import datetime, timedelta, date
from django.apps import apps
from django.db.models import Sum


class AccountingObj(object):
    def __init__(self, manager_name, app):
        self.manager_name = manager_name
        self.app = app

    def update_trial_balance(self, params):
        # print("=1"*10)
        # print(params)
        app_ = params["app"]

        accounting_web = apps.get_model(app_label=app_, model_name=app_ + "web")
        timedim = apps.get_model(app_label=app_, model_name="timedim")
        location = apps.get_model(app_label=app_, model_name="locations")

        company_obj_id_ = params["company_obj_id"]
        gld_table_name_ = params["gld_table_name"]
        tb_table_name_ = params["tb_table_name"]
        model_tb = apps.get_model(app_label=app_, model_name=tb_table_name_)
        start_date_dim = params["start_date"]
        end_date_dim = params["end_date"]
        model_gld = apps.get_model(app_label=app_, model_name=gld_table_name_)
        gld_objs = model_gld.objects.filter(generalledger__time_dim__id__gte=start_date_dim,
                                            generalledger__time_dim__id__lte=end_date_dim,
                                            accounting_web__id=company_obj_id_)\
            .exclude(generalledger__comment__icontains="BB").values('accounting_web',
                                                                    'generalledger__location',
                                                                    'generalledger__time_dim__id',
                                                                    'account').annotate(
            amount=Sum('amount')).all()

        # print("=3"*10)
        # print(gld_objs)
        # print("=4"*10)

        for q in gld_objs:
            # print("accounting_web", q["accounting_web"])
            # print("generalledger__location", q["generalledger__location"])
            # print("generalledger__time_dim__id", q["generalledger__time_dim__id"])
            # print("account", q["account"])
            # print("amount", q["amount"])
            # print("=5"*10)
            try:
                accounting_web_obj = accounting_web.objects.get(id=q["accounting_web"])
                timedim_obj = timedim.objects.get(id=q["generalledger__time_dim__id"])
                location_obj = location.objects.get(id=q["generalledger__location"])
                # print("=6"*10)
                # print(accounting_web_obj)
                # print("=7"*10)
                tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj,
                                                           location=location_obj,
                                                           time_dim=timedim_obj,
                                                           level=1,  account=q["account"]
                )
                tb_obj.amount =q["amount"]
                tb_obj.save()
            except Exception as ex:
                print(ex)

        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)
        # print(model_tb)
        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)

        gld_objs = model_gld.objects.filter(generalledger__time_dim__id__gte=start_date_dim,
                                            generalledger__time_dim__id__lte=end_date_dim,
                                            accounting_web__id=company_obj_id_,
                                            generalledger__comment__icontains="BB").values('accounting_web',
                                                                                           'generalledger__location',
                                                                                           'generalledger__time_dim__id',
                                                                                           'account').annotate(
            amount=Sum('amount')).all()

        for q in gld_objs:
            try:
                accounting_web_obj = accounting_web.objects.get(id=q["accounting_web"])
                timedim_obj = timedim.objects.get(id=q["generalledger__time_dim__id"])
                location_obj = location.objects.get(id=q["generalledger__location"])
                tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj,
                                                           location=location_obj,
                                                           time_dim=timedim_obj,
                                                           level=0,  account=q["account"]
                )
                tb_obj.amount = q["amount"]
                tb_obj.save()
                # print(tb_obj)
            except Exception as ex:
                print(ex)

        gld_objs = model_gld.objects.filter(generalledger__time_dim__id__gte=start_date_dim,
                                            generalledger__time_dim__id__lte=end_date_dim,
                                            accounting_web__id=company_obj_id_).values('accounting_web',
                                                                    'generalledger__location',
                                                                    'generalledger__time_dim__year',
                                                                    'generalledger__time_dim__month',
                                                                    'account').annotate(
            amount=Sum('amount')).all()

        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)
        # print(gld_objs)
        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)

        for q in gld_objs:
            try:
                accounting_web_obj = accounting_web.objects.get(id=q["accounting_web"])
                y_ = q["generalledger__time_dim__year"]
                m_ = q["generalledger__time_dim__month"]
                ds_ = (date(y_, m_+1, 1) - date(y_, m_, 1)).days
                time_dim_id = y_*10000+m_*100+ds_
                timedim_obj, c = timedim.objects.get_or_create(id=time_dim_id)
                if c:
                    timedim_obj.year = y_
                    timedim_obj.month = m_
                    if m_ > 9:
                        timedim_obj.quarter = 4
                    elif m_ > 6:
                        timedim_obj.quarter = 3
                    elif m_ > 3:
                        timedim_obj.quarter = 2
                    else:
                        timedim_obj.quarter = 1
                    timedim_obj.day = 0
                    timedim_obj.save()
                location_obj = location.objects.get(id=q["generalledger__location"])
                tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj,
                                                           location=location_obj,
                                                           time_dim=timedim_obj,
                                                           level=2,  account=q["account"]
                )
                tb_obj.amount = q["amount"]
                tb_obj.save()
                # print(tb_obj)
                # print(tb_obj)
            except Exception as ex:
                print(ex)

        # print("=5"*10)
        return {"start date": start_date_dim, "end date": end_date_dim}

    def set_time_dimension(self, params):
        # print(params)
        app_ = params["app"]
        table_name_ = params["table_name"]
        model = apps.get_model(app_label=app_, model_name=table_name_)
        date_from = datetime.now() + timedelta(days=-365)
        for i in range(4020):
            date_to = date_from + timedelta(days=i)
            pky = date_to.year*10000+date_to.month*100+date_to.day  #
            if date_to.month >= 10:
                q = 4
            elif date_to.month >= 7:
                q = 3
            elif date_to.month >= 4:
                q = 2
            else:
                q = 1
            d, c = model.objects.get_or_create(id=pky, year=date_to.year, quarter=q, month=date_to.month,
                                               day=date_to.day)
        return {"last_date": pky}

