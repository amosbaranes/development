from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
import os
from django.db.models import Q
import pandas as pd
import numpy as np
from openpyxl.utils.dataframe import dataframe_to_rows
from django.db import connection
from django.utils.translation import get_language
# --
from .models import (RBOIC, CountryRegion, CountryRating, Country, GlobalIndustryAverages,
                     Industry ,CompanyInfo, CompanyData, Project)
from ..core.sql import SQL


# Fix game_id.  should use project_id
def home(request, obj_id):
    industry = Industry.objects.exclude(sic_description='0').all()
    global_industry_averages = GlobalIndustryAverages.objects.all()
    project = Project.objects.filter(translations__language_code=get_language()).get(id=obj_id)
    country = Country.objects.all()
    companies = CompanyInfo.objects.exclude(company_name='0').all()
    return render(request, 'corporatevaluation/home.html',
                  {'industry': industry,
                   'global_industry_averages': global_industry_averages,
                   'project': project,
                   'country': country,
                   'companies': companies,
                   })


def get_companies_valuation_actual(request):
    sic_code=request.POST.get('sic_code')
    year=request.POST.get('year')
    i = None
    if int(sic_code) == 1:
        companies_ = CompanyData.objects.exclude(year=year, company_name='0').all()
    else:
        i = Industry.objects.get(sic_code=sic_code)
        # print(i)
        companies_ = CompanyData.objects.filter(year=year, company__industry_id=i).select_related('company').all()

    for c in companies_:
        print('----')
        print(c.company.company_name, c.iv_per_share)
        print('----')


    # q = cs.values('iv_per_share')
    # df = pd.DataFrame.from_records(q)

    return render(request, 'corporatevaluation/companies_valuation_vs_actual.html',
                  {'industry': i,
                   'companies': companies_
                   })


def configure_corporatevaluation_project(request, game):
    pass


def get_interest_coverage_ratio(request):
    try:
        icr=float(request.POST.get('icr'))
        if icr <= -100000.0:
            icr = -1000.0
        if icr >= 100000.0:
            icr = 1000.0
        o = RBOIC.objects.filter(to_ic__gte=icr).filter(from_ic__lte=icr).all()[0]
        data = {'rating': o.rating, 'spread': o.spread}
    except Exception as ex:
        data = {'rating': 'nan', 'spread': 'nan'}
    return JsonResponse(data)


def get_industry_detail(request):
    sic_code=request.POST.get('sic_code')
    if int(sic_code) == 1:
        cs = CompanyInfo.objects.exclude(company_name='0').all()
    else:
        i = Industry.objects.get(sic_code=sic_code)
        # print(i)
        cs = CompanyInfo.objects.filter(industry=i).all()

    ss = "0;-------"
    for c in cs:
        ss += "[+]" + str(c.id) + ";" + c.company_name
    data = {'status': ss}
    return JsonResponse(data)


def set_default(v):
    try:
        v = round(v)
    except Exception as e:
        pass
    return v


def get_company_detail(request):
    sid = request.POST.get('id')
    c = CompanyInfo.objects.get(id=sid)
    lll = {}
    for cd in c.company_data.all():

        try:
            _return_on_equity = round(100 * (cd.number_of_shares * cd.share_price / cd.p_over_e_ratio)) / 100
        except Exception as e:
            _return_on_equity = 0

        try:
            _eps = round(100 * cd.share_price / cd.p_over_e_ratio) / 100
        except Exception as e:
            _eps = 0

        try:
            _debt_to_total_equity = round(100 * cd.total_long_term_debt / cd.stockholders_equity) / 100
        except Exception as e:
            _debt_to_total_equity = 0

        try:
            _book_value_ratio = round(100 * cd.stockholders_equity / cd.number_of_shares) / 100
        except Exception as e:
            _book_value_ratio = 0

        try:
            _times_interest_earned = round(100 * cd.ebit / cd.interest_expense) / 100
        except Exception as e:
            _times_interest_earned = 0

        try:
            _net_profit_on_sales = round(100 * (cd.ebit - cd.income_taxes - cd.interest_expense) / cd.revenue) / 100
        except Exception as e:
            _net_profit_on_sales = 0

        ll = {
              # Balance Sheet
              # Current Assets
              'cash_cash_equivalents': (set_default(cd.cash_cash_equivalents), 'Cash & Equivalents'),
              'goodwill': (set_default(cd.goodwill), 'Goodwill'),
              'intangible_assets_net': (set_default(cd.intangible_assets_net), 'Intangible Assets(net)'),
              # Debt
              'noncurrent_liabilities': (set_default(cd.noncurrent_liabilities), 'Long-term Liabilities'),
              'long_term_debt_noncurrent': (set_default(cd.long_term_debt_noncurrent), 'LT Liabilities (Non-Current)'),
              'total_long_term_debt': (set_default(cd.total_long_term_debt), 'Total long term debt'),
              # Equity
              'equity_attributable_to_oncontrolling_interest': (set_default(cd.equity_attributable_to_oncontrolling_interest), 'Minority Interest'),
              'preferred_stock': (set_default(cd.preferred_stock), 'Preferred Stocks'),
              'stockholders_equity': (set_default(cd.stockholders_equity), 'Stockholders Equity'),
              # Income Statement
              'revenue': (set_default(cd.revenue), 'Revenues'),
              'ebit': (set_default(cd.ebit), 'EBIT'),

              'ebitda': (set_default(cd.ebitda), 'EBITDA'),
              'interest_expense': (set_default(cd.interest_expense), 'Interest Expense'),
              'income_taxes': (set_default(cd.income_taxes), 'Income Taxes'),


              # Other Information
              'share_price': (set_default(cd.share_price), 'Share Price'),
              'market_value_equity': (set_default(cd.market_value_equity), 'MV of Equity'),
              'enterprise_value': (set_default(cd.enterprise_value), 'Enterprise Value'),
              'number_of_shares': (set_default(cd.number_of_shares), '# of Shares'),
              # Ratios
              # -------------
              # current ratio
              #> quick ratio
              #> Debt to Total Assets
              'times_interest_earned': (_times_interest_earned, 'Times Interest Earned'),
              #> Account Receivable
              #> Inventory
              'net_profit_on_sales': (_net_profit_on_sales, 'Net Profit on Sales'),
              # Gross Profit Margin
              # Return on Assets
              # 'return_on_assets': (round(100*(cd.ebit)/cd.interest_expense)/100, 'Return on Assets'),

              'return_on_equity': (_return_on_equity, 'Return On Equity'),

              'eps': (_eps, 'EPS'),
              'p_over_e_ratio': (set_default(cd.p_over_e_ratio), 'P/E'),
              #> Dividend Rate/Yield
              #> Dividend Payout
              'book_value_ratio': (_book_value_ratio, 'Book Value Ratio'),
              #
              'p_over_s_ratio': (set_default(cd.p_over_s_ratio), 'P/S'),
              'p_over_b_ratio': (set_default(cd.p_over_b_ratio), 'P/B'),
              'p_over_cash_flow_ratio': (set_default(cd.p_over_cash_flow_ratio), 'P/CF'),
              'p_over_ebitda_ratio': (set_default(cd.p_over_ebitda_ratio), 'P/EBITDA'),
              'debt_to_total_equity': (_debt_to_total_equity, 'Debt to Total Equity'),
              'interest_coverage_ratio': (set_default(cd.interest_coverage_ratio_calculated), 'Interest Coverage Ratio'),
              'effective_tax_rate': (set_default(cd.effective_tax_rate), 'Effective Tax Rate'),
              'ev_over_revenue': (set_default(cd.ev_over_revenue), 'EV Over Revenue')
        }
        # print(cd.year)
        lll[cd.year] = ll
    # print(lll)

    country_id = Country.objects.get(country='United States').id
    data = {'ticker': c.ticker, 'sic_code': c.industry.sic_code, 'country_id': country_id,
            'sic_description': c.industry.sic_description, 'company_data': lll}
    return JsonResponse(data)


def wacc_ebit_roic(request):
    title = _('wacc_ebit_roic')
    return render(request, 'corporatevaluation/wacc_ebit_roic.html', {'title': title})


def team(request):
    title = _('CVTeam')
    return render(request, 'corporatevaluation/team.html', {'title': title})


def truncate_and_get_df_from_excel(table=None, file_name=None):
    table.truncate()
    wd = os.getcwd()
    s_dir = wd + '/academycity/apps/corporatevaluation/data/'
    sr = s_dir + file_name
    df = pd.read_excel(sr, 'Data')
    return dataframe_to_rows(df, index=False, header=False)


def update_data(request):
    # print('update_data 1')
    dic = {'status': 'ok'}
    try:
        for r in truncate_and_get_df_from_excel(table=RBOIC, file_name='RatingBasedOnInterestCoverage.xlsx'):
            RBOIC.objects.create(from_ic=float(r[0]),
                                 to_ic=float(r[1]), rating=r[2], spread=float(r[3]))

        for r in truncate_and_get_df_from_excel(table=CountryRegion, file_name='CountryRegion.xlsx'):
            CountryRegion.objects.create(region=r[0])

        for r in truncate_and_get_df_from_excel(table=CountryRating, file_name='CountryRating.xlsx'):
            CountryRating.objects.create(country_rating=r[0], default_spread=float(r[1]))

        for r in truncate_and_get_df_from_excel(table=Country, file_name='Country.xlsx'):
            try:
                cr = CountryRating.objects.filter(country_rating=r[2]).all()[0]
                cre = CountryRegion.objects.filter(region=r[3]).all()[0]
                Country.objects.create(country=r[0], marginal_tax_rate=float(r[1]), long_term_rating=cr, region=cre)
            except Exception as e:
                print(e)

        for r in truncate_and_get_df_from_excel(table=GlobalIndustryAverages, file_name='GlobalIndustryAverages.xlsx'):
            try:
                GlobalIndustryAverages.objects.create(industry_name=r[0], number_of_firms=float(r[1]),
                                                      unlevered_beta_corrected_for_cash=r[2],
                                                      market_d_over_e_ratio=r[3], market_debt_to_capital=r[4],
                                                      effective_tax_rate=r[5], dividend_payout=r[6], net_margin=r[7],
                                                      pre_tax_operating_margin=r[8],
                                                      roe=r[9], roic=r[10], SalesOverCapital=r[11], ev_over_sales=r[12],
                                                      revenue_growth_rateLast_5_years=r[13],
                                                      expected_earnings_growth_next_5_years=r[14]
                                                      )
            except Exception as e:
                print(e)

        Industry.truncate()
        CompanyInfo.truncate()
        for r in truncate_and_get_df_from_excel(table=CompanyData, file_name='Companies.xlsx'):
            try:
                industry_, created = Industry.objects.get_or_create(sic_code=r[2])
                if created:
                    industry_.sic_description = r[3]
                    industry_.save()
                CompanyInfo.objects.create(ticker=r[0], cik=r[1], industry=industry_, company_name=r[4],
                                           city=r[5], state=r[6], zip=r[7])
            except Exception as e:
                print(e)

    except Exception as exc:
        print(exc)

    return JsonResponse(dic)


def update_account(request):
    dic = {'status': 'ok'}
    year_ = request.POST.get('year')
    account_ = request.POST.get('account')
    ticker_ = request.POST.get('ticker')
    amount_ = request.POST.get('amount')
    c = CompanyData.objects.get(Q(year = year_), Q(company__ticker = ticker_))
    setattr(c, account_, amount_)
    c.save()
    dic["result"] = getattr(c, account_)

    return JsonResponse(dic)


def update_data_year(request, name_, game, team_, s_url):
    sql = SQL()
    nyear = request.POST.get('nyear')
    # print(nyear)
    s_status = 'ok: ' + str(nyear)
    dic = {'status': s_status}
    if nyear == 2012:
        CompanyData.objects.all().delete()
    else:
        ssql = "DELETE FROM corporatevaluation_companydata WHERE year = %s"
        data = [str(nyear)]
        # print('-----------')
        # print(ssql)
        # print(data)
        count = sql.exc_sql(ssql, data)
        # print(count)

    wd = os.getcwd()
    sdata = wd + '/academycity/apps/corporatevaluation/data/'
    sr = sdata + str(nyear) + '.xlsx'

    # print('-'*100)
    # print(sr)
    # print('-'*100)

    df = pd.read_excel(sr, 'Data')

    # print(df)

    # nnn_ = 0
    for r in dataframe_to_rows(df, index=False, header=False):
        try:
            c_ = CompanyInfo.objects.filter(ticker=r[0]).all()[0]
            CompanyData.objects.create(company=c_,
                                       year=nyear,
                                       ebit=round(r[1], 0),
                                       number_of_shares=int(r[2]),
                                       share_price=round(r[3], 2),
                                       cash_cash_equivalents=round(r[4], 0),
                                       preferred_stock=round(r[5], 0),
                                       market_value_equity=round(r[6], 0),
                                       noncurrent_liabilities=round(r[7], 0),
                                       long_term_debt_noncurrent=round(r[8], 0),
                                       equity_attributable_to_oncontrolling_interest=round(r[9], 0),
                                       revenue=round(r[10], 0),
                                       interest_expense=round(r[11], 0),
                                       income_taxes=round(r[12], 0),
                                       effective_tax_rate=round(r[13], 4),
                                       interest_coverage_ratio=round(r[14], 4),
                                       total_long_term_debt=round(r[15], 0),
                                       intangible_assets_net=round(r[16], 0),
                                       goodwill=round(r[17], 0),
                                       enterprise_value=round(r[18], 0),
                                       ev_over_revenue=round(r[19], 4),
                                       ebitda=round(r[20], 0),
                                       p_over_e_ratio=round(r[21], 4),
                                       p_over_s_ratio=round(r[22], 4),
                                       p_over_b_ratio=round(r[23], 4),
                                       p_over_cash_flow_ratio=round(r[24], 4),
                                       p_over_ebitda_ratio=round(r[25], 4),
                                       stockholders_equity=round(r[26], 0)
                                       )
        except Exception as e:
            dic = {'status': 'ko5'}
            # if nnn_ < 10:
            #     print(5)
            #     print(r)
            #     print(e)
            #     nnn_ += 1


    return JsonResponse(dic)


def get_screens_data(request, name_, s_url):
    pass


def get_screens_inputs(request, name_, s_url):
    print('---')
    print(s_url)
    print('---')

    industry = Industry.objects.exclude(sic_description='0').all()
    global_industry_averages = GlobalIndustryAverages.objects.all()
    country = Country.objects.all()
    companies = CompanyInfo.objects.exclude(company_name='0').all()
    return render(request, s_url,
                  {'name': name_,
                   'industry': industry,
                   'global_industry_averages': global_industry_averages,
                   'country': country,
                   'companies': companies,
                   'user': request.user,
                   })


def get_screens(request):
    name_ = request.POST.get('name').lower()
    # print(name_)
    # obj_id = request.POST.get('obj_id')  # obj_id is the game_id
    # game = Game.objects.filter(translations__language_code=get_language()).get(id=obj_id)

    # team_ = game.get_current_team(request.user)

    s_url = 'corporatevaluation/simulation/_' + name_ + '.html'
    sr = "get_screens_"+name_+"(request, name_, s_url)"
    # print(sr)
    #
    #     https://python-reference.readthedocs.io/en/latest/docs/functions/eval.html
    # >>> # this example shows how providing globals argument prevents eval from accessing real globals dictionary
    # >>> eval("os.getcwd()", {})
    # NameError: name 'os' is not defined
    # >>> # that example however can be bypassed by using __import__ function inside eval
    # >>> eval('__import__("os").getcwd()', {})

    # create_action(request.user, 'globsim__get_screens__' + name_, target=game)
    return eval(sr)

