from datetime import date, timedelta
import copy
from datetime import datetime
import pandas as pd

from django.shortcuts import get_object_or_404
from ..courses.models import GeneralLedger, ChartOfAccounts
from .utils import get_number, add_years_months_days
from .sql import SQL


# gl_entries = [(account, amount), ]
def post_gl(gl_entries):
    sub_transaction_number = 1
    source = 1
    transaction_number = get_number(1)
    for gle in gl_entries:
        a = get_object_or_404(ChartOfAccounts, id=gle[0])
        # print(gle)

        glp = GeneralLedger.objects.create(transaction=transaction_number,
                                           sub_transaction=sub_transaction_number,
                                           account=a,
                                           amount=gle[1],
                                           target=gle[2],
                                           )
        sub_transaction_number += 1
    return 1


    # PERIOD_TYPES = (
    #     (0, 'Other'),
    #     (1, 'day'),
    #     (2, 'month'),
    #     (3, 'year'),
    # )
    #
    # FLOW_TYPES = (
    #     (0, 'Other'),
    #     (1, 'flow'),
    #     (2, 'cumulative'),
    # )


def update_trial_balance(ll):
    # print(from_date)
    sql = SQL()
    if '1' in ll and '2' in ll and '3' in ll:
        sql.exc_sql("""truncate table courses_trialbalance""", ())
    else:
        if '1' in ll:
            sql.exc_sql("""delete from courses_trialbalance where period_type = 1""", ())
        elif '2' in ll:
            sql.exc_sql("""delete from courses_trialbalance where period_type = 2""", ())
        elif '3' in ll:
            sql.exc_sql("""delete from courses_trialbalance where period_type = 3""", ())

    from_date_ = GeneralLedger.objects.earliest('created').created
    from_date = copy.copy(from_date_)
    today_end = add_years_months_days(date.today(), years=0, months=0, days=1)
    if '1' in ll:
        while from_date < today_end:
            print('000-------')
            print(from_date_)
            print(from_date)
            print('000-------')
            create_trial_balance_(period_type=1, for_beginning_date=from_date, from_date_=from_date_)
            from_date = add_years_months_days(from_date, years=0, months=0, days=1)

    if '2' in ll:
        from_month = from_date.replace(day=1)
        today_end_month = add_years_months_days(date.today().replace(day=1), years=0, months=1, days=0)
        while from_month < today_end_month:
            create_trial_balance_(period_type=2, for_beginning_date=from_month, from_date_=from_date_)
            from_month = add_years_months_days(from_month, years=0, months=1, days=0)

    if '3' in ll:
        from_year = date(from_date.year, 1, 1)
        today_end_year = add_years_months_days(date(date.today().year,1,1), years=1, months=0, days=0)
        while from_year < today_end_year:
            create_trial_balance_(period_type=3, for_beginning_date=from_year, from_date_=from_date_)
            from_year = add_years_months_days(from_year, years=1, months=0, days=0)


# period_type, flow_type, for_date, account, Amount
def create_trial_balance_(period_type, for_beginning_date, from_date_):
    print('0001----------')
    print(from_date_)
    print(for_beginning_date)
    print('0001----------')
    for_end_date = None

    if period_type == 1:
        for_end_date = add_years_months_days(for_beginning_date, years=0, months=0, days=1)
        pkey_date = for_beginning_date.year*10000 + for_beginning_date.month*100 + for_beginning_date.day

        for_beginning_date_1 = add_years_months_days(for_beginning_date, years=0, months=0, days=-1)
        pkey_date_1 = for_beginning_date_1.year*10000 + for_beginning_date_1.month*100 + for_beginning_date_1.day

        pkey_from_date_ = from_date_.year*10000 + from_date_.month*100 + from_date_.day
    elif period_type == 2:
        for_end_date = add_years_months_days(for_beginning_date, years=0, months=1, days=0)
        pkey_date = for_beginning_date.year*10000 + for_beginning_date.month*100

        for_beginning_date_1 = add_years_months_days(for_beginning_date, years=0, months=-1, days=0)
        pkey_date_1 = for_beginning_date_1.year*10000 + for_beginning_date_1.month*100

        pkey_from_date_ = from_date_.year*10000 + from_date_.month*100
    elif period_type == 3:
        for_end_date = add_years_months_days(for_beginning_date, years=1, months=0, days=0)
        pkey_date = for_beginning_date.year*10000

        for_beginning_date_1 = add_years_months_days(for_beginning_date, years=-1, months=0, days=0)
        pkey_date_1 = for_beginning_date_1.year*10000

        pkey_from_date_ = from_date_.year*10000
    # --- sum all records for the period


    print('---pkey_from_date_-----')
    print(pkey_from_date_)
    print(pkey_date)
    print(pkey_date_1)
    print('--------')

    sql = SQL()
    ssql_ = """
    insert into courses_trialbalance (period_type, flow_type, pkey_date, account_id, amount)
    select %s, %s, %s, a.account_id, a.amount
    from
    (Select g.account_id, sum(amount) as amount 
     from courses_generalledger as g
     where created >= %s and created < %s 
     Group by account_id) a
    """
    data_ = (period_type, 1, pkey_date, for_beginning_date, for_end_date)

    print('1------------')
    print(ssql_)
    print(data_)
    print('------------')
    count = sql.exc_sql(ssql_, data_)
    print(count)
    print('-----------')

    # - closing entry. not needed in BI dimension
    ssql_ = """
    insert into courses_trialbalance (period_type, flow_type, pkey_date, account_id, amount)
    select %s, %s, %s, 11, a.amount
    from
    (select sum(t.amount) as amount
    from courses_trialbalance t, courses_chartofaccounts c
    where t.pkey_date = %s and
    t.account_id = c.id and
    c.account_type = 3) a
    
    """
    data_ = (period_type, 1, pkey_date, pkey_date)

    print('2.1------------')
    print(ssql_)
    print(data_)
    print('------------')
    count = sql.exc_sql(ssql_, data_)
    print(count)
    print('-----------')

    ##-----
    ssql_ = """
    insert into courses_trialbalance (period_type, flow_type, pkey_date, account_id, amount)
    select %s, %s, %s, 12, a.amount
    from
    (select -sum(t.amount) as amount
    from courses_trialbalance t, courses_chartofaccounts c
    where t.pkey_date = %s and
    t.account_id = c.id and
    c.account_type = 3) a

    """
    data_ = (period_type,1, pkey_date, pkey_date)

    print('2.2------------')
    print(ssql_)
    print(data_)
    print('------------')
    count = sql.exc_sql(ssql_, data_)
    print(count)
    print('-----------')

    # #-- cumulative calculation for beginning balance. notice, in the way I added the closing entry
    # #    I can ignore the income statement accounts

    print('000000')
    print(str(pkey_date))
    print(str(pkey_from_date_))
    print('000000')

    if pkey_date == pkey_from_date_:
        ssql_ = """
        insert into courses_trialbalance (period_type, flow_type, pkey_date, account_id, amount)
        Select t.period_type, %s as flow_type, t.pkey_date, t.account_id, t.amount 
        from courses_trialbalance as t, courses_chartofaccounts c
        where t.account_id = c.id and
        c.account_type = 2 and
        t.pkey_date = %s
        """
        print('0000001')
        print(str(pkey_date))
        print(str(pkey_from_date_))
        print('0000001')

        data_ = (2, pkey_from_date_)

        print('3.1------------')
        print(str(pkey_from_date_))
        print(ssql_)
        print(data_)
        print('------------')
        count = sql.exc_sql(ssql_, data_)
        print(count)
        print('-----------')
    else:
        ssql_ = """
        insert into courses_trialbalance (period_type, flow_type, pkey_date, account_id, amount)   
        select a.period_type, a.flow_type, a.pkey_date, a.account_id, sum(a.amount) as amount
        from
        (Select t.period_type, %s as flow_type, %s as pkey_date, t.account_id, t.amount 
         from courses_trialbalance as t, courses_chartofaccounts c
         where t.account_id = c.id and
         ((t.pkey_date =  %s and t.flow_type = 1) or
          (t.pkey_date =  %s and t.flow_type = 2 and c.account_type = 2))) a
          group by a.period_type, a.flow_type, a.pkey_date, a.account_id
        """

        data_ = (2, pkey_date, pkey_date, pkey_date_1)

        print('3.2------------')
        print(ssql_)
        print(data_)
        print('------------')
        count = sql.exc_sql(ssql_, data_)
        print(count)
        print('-----------')

    sql.exc_sql("""delete from courses_trialbalance where abs(amount) < 0.001""", ())

