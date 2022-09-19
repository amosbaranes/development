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
        period_ = params["period"]
        company_obj_id_ = params["company_obj_id"]
        gld_table_name_ = params["gld_table_name"]
        tb_table_name_ = params["tb_table_name"]
        model_tb = apps.get_model(app_label=app_, model_name=tb_table_name_)
        model_gld = apps.get_model(app_label=app_, model_name=gld_table_name_)

        gld_objs = model_gld.objects.filter(period=period_, team__businesssimm_web__id=company_obj_id_)\
            .exclude(generalledger__comment__icontains="BB").values('generalledger__team',
                                                                    'period',
                                                                    'account').annotate(
            amount=Sum('amount')).all()

        # print("=3"*10)
        # print(gld_objs)
        # print("=4"*10)

        for q in gld_objs:
            try:
                tb_obj, c = model_tb.objects.get_or_create(team=generalledger__team,
                                                           period=q["period"],
                                                           level=1,
                                                           account=q["account"]
                                                           )
                tb_obj.amount = q["amount"]
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

        gld_objs = model_gld.objects.filter(period=period_, team__businesssimm_web__id=company_obj_id_,
                                            generalledger__comment__icontains="BB").values('generalledger__team',
                                                                                           'period',
                                                                                           'account').annotate(
            amount=Sum('amount')).all()

        for q in gld_objs:
            try:
                tb_obj, c = model_tb.objects.get_or_create(team=generalledger__team,
                                                           period=q["period"],
                                                           level=0,
                                                           account=q["account"]
                                                           )
                tb_obj.amount = q["amount"]
                tb_obj.save()
            except Exception as ex:
                print(ex)

        gld_objs = model_gld.objects.filter(period=period_, team__businesssimm_web__id=company_obj_id_)\
            .values('generalledger__team', 'period', 'account').annotate(amount=Sum('amount')).all()

        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)
        # print(gld_objs)
        # print("+31"*10)
        # print("+31"*10)
        # print("+31"*10)

        for q in gld_objs:
            try:
                tb_obj, c = model_tb.objects.get_or_create(team=generalledger__team,
                                                           period=q["period"],
                                                           level=2,
                                                           account=q["account"]
                                                           )
                tb_obj.amount = q["amount"]
                tb_obj.save()
                # print(tb_obj)
                # print(tb_obj)
            except Exception as ex:
                print(ex)

        # print("=5"*10)
        return {"start date": start_date_dim, "end date": end_date_dim}
