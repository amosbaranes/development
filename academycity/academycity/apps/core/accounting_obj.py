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
        # print("=1"*10)
        # print("=1"*10)
        # print("=1"*10)
        # print(params)
        app_ = params["app"]

        accounting_web = apps.get_model(app_label=app_, model_name=app_ + "web")
        timedim = apps.get_model(app_label=app_, model_name="timedim")
        location = apps.get_model(app_label=app_, model_name="locations")

        # print("=2"*10)
        # print("=2"*10)
        # print("=2"*10)
        # print("=2"*10)
        company_obj_id_ = params["company_obj_id"]
        gld_table_name_ = params["gld_table_name"]
        tb_table_name_ = params["tb_table_name"]
        model_tb = apps.get_model(app_label=app_, model_name=tb_table_name_)
        try:
            model_tb.truncate()
        except Exception as ex:
            print("9076 " + str(ex))

        start_date_dim = params["start_date"]
        end_date_dim = params["end_date"]
        model_gld = apps.get_model(app_label=app_, model_name=gld_table_name_)
        sql = SQL()
        squery = '''
                SELECT gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account, sum(amount) as amount
                FROM accounting_GeneralLedgerDetail gld, accounting_GeneralLedgers gl
                WHERE gl.id = gld.generalledger_id and gl.comment NOT LIKE '%%BB%%' and
                  gl.time_dim_id >= ''' + start_date_dim + " and gl.time_dim_id <= " + end_date_dim + '''
                GROUP BY gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account
                ORDER BY gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account
                '''
        # print(squery)
        results = sql.exc_sql(squery, [], verb='select')
        # print(results)
        for k in results:
            # print(k)
            accounting_web_obj = accounting_web.objects.get(id=k[0])
            location_obj = location.objects.get(id=k[1])
            timedim_obj = timedim.objects.get(id=k[2])
            tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj, location=location_obj,
                                                       time_dim=timedim_obj, level=1,  account=k[3])
            tb_obj.amount = k[4]
            tb_obj.save()

        # gld_objs = model_gld.objects.values('accounting_web', 'generalledger__location', 'generalledger__time_dim__id',
        #                                     'account').filter(generalledger__time_dim__id__gte=start_date_dim,
        #                                                       generalledger__time_dim__id__lte=end_date_dim,
        #                                                       accounting_web__id=company_obj_id_).\
        #     exclude(generalledger__comment__icontains="BB").annotate(amount=Sum('amount'))

        squery = '''
                SELECT gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account, sum(amount) as amount
                FROM accounting_GeneralLedgerDetail gld, accounting_GeneralLedgers gl
                WHERE gl.id = gld.generalledger_id and gl.comment LIKE '%%BB%%' and
                  gl.time_dim_id >= ''' + start_date_dim + " and gl.time_dim_id <= " + end_date_dim + '''
                GROUP BY gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account
                ORDER BY gl.accounting_web_id, gl.location_id, gl.time_dim_id, gld.account
                '''
        # print(squery)
        results = sql.exc_sql(squery, [], verb='select')
        # print(results)
        for k in results:
            # print(k)
            # print(k[0])
            accounting_web_obj = accounting_web.objects.get(id=k[0])
            location_obj = location.objects.get(id=k[1])
            timedim_obj = timedim.objects.get(id=k[2])
            tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj,
                                                       location=location_obj,
                                                       time_dim=timedim_obj,
                                                       level=0,  account=k[3]
            )
            tb_obj.amount = k[4]
            tb_obj.save()

        squery = '''
                SELECT gl.accounting_web_id, gl.location_id, td.year, td.month,
                       gld.account, sum(gld.amount) as amount
                FROM accounting_GeneralLedgerDetail gld, accounting_GeneralLedgers gl,
                     accounting_timedim td
                WHERE gl.id = gld.generalledger_id and gl.time_dim_id=td.id and
                  td.id >= ''' + start_date_dim + " and td.id <= " + end_date_dim + '''
                GROUP BY gl.accounting_web_id, gl.location_id, td.year, td.month, gld.account
                ORDER BY gl.accounting_web_id, gl.location_id, td.year, td.month, gld.account
                '''
        # print(squery)
        try:
            results = sql.exc_sql(squery, [], verb='select')
        except Exception as ex:
            print("Error 2030: "+str(ex))
        # print(results)
        for k in results:
            # print(k)
            accounting_web_obj = accounting_web.objects.get(id=k[0])
            location_obj = location.objects.get(id=k[1])
            td_ = k[2]*10000+k[3]*100+(date(k[2], k[3]+1, 1) - date(k[2], k[3], 1)).days
            timedim_obj, c = timedim.objects.get_or_create(id=td_)
            if c:
                timedim_obj.year = k[2]
                timedim_obj.month = k[3]
                if k[3] > 9:
                    timedim_obj.quarter = 4
                elif k[3] > 6:
                    timedim_obj.quarter = 3
                elif k[3] > 3:
                    timedim_obj.quarter = 2
                else:
                    timedim_obj.quarter = 1
                timedim_obj.day = (date(k[2], k[3]+1, 1) - date(k[2], k[3], 1)).days
                timedim_obj.save()

            tb_obj, c = model_tb.objects.get_or_create(accounting_web=accounting_web_obj,
                                                       location=location_obj,
                                                       time_dim=timedim_obj,
                                                       level=2,  account=k[4]
            )
            tb_obj.amount = k[5]
            tb_obj.save()

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

