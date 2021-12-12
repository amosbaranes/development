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
                     CompanyData, Project, ToDoList,
                     XBRLValuationAccounts, XBRLValuationAccountsMatch,
                     XBRLIndustryInfo, Industry,
                     XBRLCompanyInfo, CompanyInfo,
                     XBRLCountryYearData, XBRLSPStatistics,
                     XBRLCountry, XBRLYearsCompanyOperations, XBRLCountriesOfOperations,
                     XBRLRegion, XBRLRegionYearData, XBRLRegionsOfOperations, XBRLIndustryBetasOfOperations)
# --

from ..core.sql import SQL
from ..webcompanies.WebCompanies import WebSiteCompany
from .xbrl_obj import AcademyCityXBRL, TDAmeriTrade, FinancialAnalysis
import datetime
import requests
from bs4 import BeautifulSoup
import re
from ..core.utils import log_debug, clear_log_debug
from django.db.models import Count
from ..core.templatetags.core_tags import has_group


# Fix game_id.  should use project_id
def home(request, obj_id):
    clear_log_debug()
    log_debug("cv_home")
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    industry = XBRLIndustryInfo.objects.exclude(sic_description='0').all()
    global_industry_averages = GlobalIndustryAverages.objects.all()
    project = Project.objects.filter(translations__language_code=get_language()).get(id=obj_id)
    XBRLCountryYearData.project = project
    XBRLRegionYearData.project = project

    request.session['cv_project_id'] = project.id

    countries_data = XBRLCountryYearData.project_objects.all()
    regions_data = XBRLRegionYearData.project_objects.all()

    companies = XBRLCompanyInfo.objects.filter(ticker__gte='9')
    if not has_group(request.user, "admins"):
        companies = companies.filter(is_active=True)
    companies = companies.all()
    log_debug("cv_home 21")

    todolist = ToDoList.objects.filter().all()
    return render(request, 'corporatevaluation/home.html',
                  {'institution_obj': company_obj,
                   'industry': industry,
                   'global_industry_averages': global_industry_averages,
                   'project': project,
                   'countries_data': countries_data,
                   'regions_data': regions_data,
                   'companies': companies,
                   'todolist': todolist,
                   })


def update_country_risk(request):
    clear_log_debug()
    ty_ = request.POST.get('ty')
    # print('ty_')
    # print(ty_)

    y_ = request.POST.get('y')
    t_ = request.POST.get('t')

    id_ = request.POST.get('id')
    # print('id_')
    # print(id_)

    if int(id_) > -1:
        if ty_ == "region":
            k = XBRLRegionsOfOperations.objects.get(id=id_).delete()
        elif ty_ == "country":
            k = XBRLCountriesOfOperations.objects.get(id=id_).delete()
        else:
            k = XBRLIndustryBetasOfOperations.objects.get(id=id_).delete()
        # print('k')
        # print(k)

    c_ = request.POST.get('c')
    # print(c_)
    if c_ == -1:
        return JsonResponse({'status': 'ok', 'id': -1})

    re_ = request.POST.get('re')
    ra_ = request.POST.get('ra')
    sp_ = request.POST.get('sp')
    rp_ = request.POST.get('rp')
    tx_ = request.POST.get('tx')
    # print(y_, t_, c_, re_, ra_, sp_, rp_, tx_)

    company = XBRLCompanyInfo.objects.get(ticker=t_)
    cy, c = XBRLYearsCompanyOperations.objects.get_or_create(company=company, year=y_)
    if ty_ == "region":
        region = XBRLRegion.objects.get(id=c_)
        co, c = XBRLRegionsOfOperations.objects.get_or_create(company_year=cy, region=region)
    elif ty_ == "country":
        country = XBRLCountry.objects.get(id=c_)
        co, c = XBRLCountriesOfOperations.objects.get_or_create(company_year=cy, country=country)
    else:
        industry = GlobalIndustryAverages.objects.get(id=c_)
        co, c = XBRLIndustryBetasOfOperations.objects.get_or_create(company_year=cy, industry=industry)

    # print(co)
    try:
        re_ = float(re_)
        co.revenues = re_
    except Exception as ex:
        log_debug(ex)

    if ty_ == "industry":
        try:
            ra_ = float(ra_)
            co.ev_over_sales = ra_
        except Exception as ex:
            log_debug(ex)
        try:
            sp_ = float(sp_)
            co.estimated_value = sp_
        except Exception as ex:
            log_debug(ex)
        try:
            rp_ = float(rp_)
            co.unlevered_beta = rp_
        except Exception as ex:
            log_debug(ex)
        try:
            tx_ = float(tx_)
            co.estimated_growth = tx_
        except Exception as ex:
            log_debug(ex)
    else:
        co.rating = ra_
        try:
            sp_ = float(sp_)
            co.spread = sp_
        except Exception as ex:
            log_debug(ex)
        try:
            rp_ = float(rp_)
            co.risk_premium = rp_
        except Exception as ex:
            log_debug(ex)
        try:
            tx_ = float(tx_)
            co.tax_rate = tx_
        except Exception as ex:
            log_debug(ex)
    try:
        co.save()
    except Exception as ex:
        log_debug(ex)

    dic = {'status': 'ok', 'id': co.id}
    return JsonResponse(dic)


def get_companies_valuation_actual(request):
    clear_log_debug()
    sic_code=request.POST.get('sic_code')
    year=request.POST.get('year')
    i = None
    if int(sic_code) == 1:
        companies_ = CompanyData.objects.exclude(year=year, company_name='0').all()
    else:
        i = Industry.objects.get(sic_code=sic_code)
        # print(i)
        companies_ = CompanyData.objects.filter(year=year, company__industry_id=i).select_related('company').all()

    # for c in companies_:
    #     print('----')
    #     print(c.company.company_name, c.iv_per_share)
    #     print('----')

    # q = cs.values('iv_per_share')
    # df = pd.DataFrame.from_records(q)

    return render(request, 'corporatevaluation/simulation/companies_valuation_vs_actual.html',
                  {'industry': i,
                   'companies': companies_
                   })


def configure_corporatevaluation_project(request, game):
    pass


def get_interest_coverage_ratio(request):
    try:
        data = {}
        for r in RBOIC.objects.all():
            data[r.id] = {"from_ic": float(r.from_ic), "to_ic": float(r.to_ic), "rating": r.rating, "spread": float(r.spread)}
    except Exception as ex:
        data = {'data': 'nan'}
    return JsonResponse(data)


def get_industry_detail(request):
    sic_code=request.POST.get('sic_code')

    cs = XBRLCompanyInfo.objects.filter(ticker__gte='9')
    if int(sic_code) != 1:
        # i = Industry.objects.get(sic_code=sic_code)
        i = XBRLIndustryInfo.objects.get(sic_code=sic_code)
        cs = cs.filter(industry=i)

    if not has_group(request.user, "admins"):
        cs = cs.filter(is_active=True)
    cs = cs.all()
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

    #
    # try:
    #     c = CompanyInfo.objects.get(ticker=xc.ticker)
    #     for cd in c.company_data.all():
    #
    #         try:
    #             _return_on_equity = round(100 * (cd.number_of_shares * cd.share_price / cd.p_over_e_ratio)) / 100
    #         except Exception as e:
    #             _return_on_equity = 0
    #
    #         try:
    #             _eps = round(100 * cd.share_price / cd.p_over_e_ratio) / 100
    #         except Exception as e:
    #             _eps = 0
    #
    #         try:
    #             _debt_to_total_equity = round(100 * cd.total_long_term_debt / cd.stockholders_equity) / 100
    #         except Exception as e:
    #             _debt_to_total_equity = 0
    #
    #         try:
    #             _book_value_ratio = round(100 * cd.stockholders_equity / cd.number_of_shares) / 100
    #         except Exception as e:
    #             _book_value_ratio = 0
    #
    #         try:
    #             _times_interest_earned = round(100 * cd.ebit / cd.interest_expense) / 100
    #         except Exception as e:
    #             _times_interest_earned = 0
    #
    #         try:
    #             _net_profit_on_sales = round(100 * (cd.ebit - cd.income_taxes - cd.interest_expense) / cd.revenue) / 100
    #         except Exception as e:
    #             _net_profit_on_sales = 0
    #
    #         ll = {
    #             # Balance Sheet
    #             # Current Assets
    #             'cash_cash_equivalents': (set_default(cd.cash_cash_equivalents), 'Cash & Equivalents'),
    #             'goodwill': (set_default(cd.goodwill), 'Goodwill'),
    #             'intangible_assets_net': (set_default(cd.intangible_assets_net), 'Intangible Assets(net)'),
    #             # Debt
    #             'noncurrent_liabilities': (set_default(cd.noncurrent_liabilities), 'Long-term Liabilities'),
    #             'long_term_debt_noncurrent': (
    #             set_default(cd.long_term_debt_noncurrent), 'LT Liabilities (Non-Current)'),
    #             'total_long_term_debt': (set_default(cd.total_long_term_debt), 'Total long term debt'),
    #             # Equity
    #             'equity_attributable_to_oncontrolling_interest': (
    #             set_default(cd.equity_attributable_to_oncontrolling_interest), 'Minority Interest'),
    #             'preferred_stock': (set_default(cd.preferred_stock), 'Preferred Stocks'),
    #             'stockholders_equity': (set_default(cd.stockholders_equity), 'Stockholders Equity'),
    #             # Income Statement
    #             'revenue': (set_default(cd.revenue), 'Revenues'),
    #             'ebit': (set_default(cd.ebit), 'EBIT'),
    #
    #             'ebitda': (set_default(cd.ebitda), 'EBITDA'),
    #             'interest_expense': (set_default(cd.interest_expense), 'Interest Expense'),
    #             'income_taxes': (set_default(cd.income_taxes), 'Income Taxes'),
    #
    #             # Other Information
    #             'share_price': (set_default(cd.share_price), 'Share Price'),
    #             'market_value_equity': (set_default(cd.market_value_equity), 'MV of Equity'),
    #             'enterprise_value': (set_default(cd.enterprise_value), 'Enterprise Value'),
    #             'number_of_shares': (set_default(cd.number_of_shares), '# of Shares'),
    #             # Ratios
    #             # -------------
    #             # current ratio
    #             # > quick ratio
    #             # > Debt to Total Assets
    #             'times_interest_earned': (_times_interest_earned, 'Times Interest Earned'),
    #             # > Account Receivable
    #             # > Inventory
    #             'net_profit_on_sales': (_net_profit_on_sales, 'Net Profit on Sales'),
    #             # Gross Profit Margin
    #             # Return on Assets
    #             # 'return_on_assets': (round(100*(cd.ebit)/cd.interest_expense)/100, 'Return on Assets'),
    #
    #             'return_on_equity': (_return_on_equity, 'Income On Equity'),
    #
    #             'eps': (_eps, 'EPS'),
    #             'p_over_e_ratio': (set_default(cd.p_over_e_ratio), 'P/E'),
    #             # > Dividend Rate/Yield
    #             # > Dividend Payout
    #             'book_value_ratio': (_book_value_ratio, 'Book Value Ratio'),
    #             #
    #             'p_over_s_ratio': (set_default(cd.p_over_s_ratio), 'P/S'),
    #             'p_over_b_ratio': (set_default(cd.p_over_b_ratio), 'P/B'),
    #             'p_over_cash_flow_ratio': (set_default(cd.p_over_cash_flow_ratio), 'P/CF'),
    #             'p_over_ebitda_ratio': (set_default(cd.p_over_ebitda_ratio), 'P/EBITDA'),
    #             'debt_to_total_equity': (_debt_to_total_equity, 'Debt to Total Equity'),
    #             'interest_coverage_ratio': (
    #             set_default(cd.interest_coverage_ratio_calculated), 'Interest Coverage Ratio'),
    #             'effective_tax_rate': (set_default(cd.effective_tax_rate), 'Effective Tax Rate'),
    #             'ev_over_revenue': (set_default(cd.ev_over_revenue), 'EV Over Revenue')
    #         }
    #         # print(cd.year)
    #         lll[cd.year] = ll
    #         country_id = 0
    #         sic_code_ = 0
    #         sic_description_ = ''
    #         country_id = Country.objects.get(country='United States').id
    #         print(country_id)
    #
    #         sic_code_ = xc.industry.sic_code
    #         print(sic_code_)
    #         sic_description_ = xc.industry.sic_description
    #     # print(lll)
    # except Exception as ex:
    #     print('ex')
    #     print(ex)
    #
    # data = {'ticker': xc.ticker, 'sic_code': sic_code_, 'country_id': country_id,
    #         'sic_description': sic_description_, 'company_data': lll}
    #
    # # country_id = Country.objects.get(country='United States').id
    # # data = {'ticker': c.ticker, 'sic_code': c.industry.sic_code, 'country_id': country_id,
    # #         'sic_description': c.industry.sic_description, 'company_data': lll}
    # return JsonResponse(data)


# Should be removed
# def get_company_detail(request):
#     lll = {}
#
#     sid = request.POST.get('id')
#     xc = XBRLCompanyInfo.objects.get(id=sid)
#     country_id = Country.objects.get(country='United States').id
#     data = {'ticker': xc.ticker, 'sic_code': xc.industry.sic_code, 'country_id': country_id,
#             'sic_description': xc.industry.sic_description, 'company_data': lll}
#
#     try:
#         c = CompanyInfo.objects.get(ticker=xc.ticker)
#         for cd in c.company_data.all():
#
#             try:
#                 _return_on_equity = round(100 * (cd.number_of_shares * cd.share_price / cd.p_over_e_ratio)) / 100
#             except Exception as e:
#                 _return_on_equity = 0
#
#             try:
#                 _eps = round(100 * cd.share_price / cd.p_over_e_ratio) / 100
#             except Exception as e:
#                 _eps = 0
#
#             try:
#                 _debt_to_total_equity = round(100 * cd.total_long_term_debt / cd.stockholders_equity) / 100
#             except Exception as e:
#                 _debt_to_total_equity = 0
#
#             try:
#                 _book_value_ratio = round(100 * cd.stockholders_equity / cd.number_of_shares) / 100
#             except Exception as e:
#                 _book_value_ratio = 0
#
#             try:
#                 _times_interest_earned = round(100 * cd.ebit / cd.interest_expense) / 100
#             except Exception as e:
#                 _times_interest_earned = 0
#
#             try:
#                 _net_profit_on_sales = round(100 * (cd.ebit - cd.income_taxes - cd.interest_expense) / cd.revenue) / 100
#             except Exception as e:
#                 _net_profit_on_sales = 0
#
#             ll = {
#                 # Balance Sheet
#                 # Current Assets
#                 'cash_cash_equivalents': (set_default(cd.cash_cash_equivalents), 'Cash & Equivalents'),
#                 'goodwill': (set_default(cd.goodwill), 'Goodwill'),
#                 'intangible_assets_net': (set_default(cd.intangible_assets_net), 'Intangible Assets(net)'),
#                 # Debt
#                 'noncurrent_liabilities': (set_default(cd.noncurrent_liabilities), 'Long-term Liabilities'),
#                 'long_term_debt_noncurrent': (
#                 set_default(cd.long_term_debt_noncurrent), 'LT Liabilities (Non-Current)'),
#                 'total_long_term_debt': (set_default(cd.total_long_term_debt), 'Total long term debt'),
#                 # Equity
#                 'equity_attributable_to_oncontrolling_interest': (
#                 set_default(cd.equity_attributable_to_oncontrolling_interest), 'Minority Interest'),
#                 'preferred_stock': (set_default(cd.preferred_stock), 'Preferred Stocks'),
#                 'stockholders_equity': (set_default(cd.stockholders_equity), 'Stockholders Equity'),
#                 # Income Statement
#                 'revenue': (set_default(cd.revenue), 'Revenues'),
#                 'ebit': (set_default(cd.ebit), 'EBIT'),
#
#                 'ebitda': (set_default(cd.ebitda), 'EBITDA'),
#                 'interest_expense': (set_default(cd.interest_expense), 'Interest Expense'),
#                 'income_taxes': (set_default(cd.income_taxes), 'Income Taxes'),
#
#                 # Other Information
#                 'share_price': (set_default(cd.share_price), 'Share Price'),
#                 'market_value_equity': (set_default(cd.market_value_equity), 'MV of Equity'),
#                 'enterprise_value': (set_default(cd.enterprise_value), 'Enterprise Value'),
#                 'number_of_shares': (set_default(cd.number_of_shares), '# of Shares'),
#                 # Ratios
#                 # -------------
#                 # current ratio
#                 # > quick ratio
#                 # > Debt to Total Assets
#                 'times_interest_earned': (_times_interest_earned, 'Times Interest Earned'),
#                 # > Account Receivable
#                 # > Inventory
#                 'net_profit_on_sales': (_net_profit_on_sales, 'Net Profit on Sales'),
#                 # Gross Profit Margin
#                 # Return on Assets
#                 # 'return_on_assets': (round(100*(cd.ebit)/cd.interest_expense)/100, 'Return on Assets'),
#
#                 'return_on_equity': (_return_on_equity, 'Income On Equity'),
#
#                 'eps': (_eps, 'EPS'),
#                 'p_over_e_ratio': (set_default(cd.p_over_e_ratio), 'P/E'),
#                 # > Dividend Rate/Yield
#                 # > Dividend Payout
#                 'book_value_ratio': (_book_value_ratio, 'Book Value Ratio'),
#                 #
#                 'p_over_s_ratio': (set_default(cd.p_over_s_ratio), 'P/S'),
#                 'p_over_b_ratio': (set_default(cd.p_over_b_ratio), 'P/B'),
#                 'p_over_cash_flow_ratio': (set_default(cd.p_over_cash_flow_ratio), 'P/CF'),
#                 'p_over_ebitda_ratio': (set_default(cd.p_over_ebitda_ratio), 'P/EBITDA'),
#                 'debt_to_total_equity': (_debt_to_total_equity, 'Debt to Total Equity'),
#                 'interest_coverage_ratio': (
#                 set_default(cd.interest_coverage_ratio_calculated), 'Interest Coverage Ratio'),
#                 'effective_tax_rate': (set_default(cd.effective_tax_rate), 'Effective Tax Rate'),
#                 'ev_over_revenue': (set_default(cd.ev_over_revenue), 'EV Over Revenue')
#             }
#             # print(cd.year)
#             lll[cd.year] = ll
#             data['company_data'] = lll
#         # print(lll)
#     except Exception as ex:
#         print('ex')
#         print(ex)
#
#     # country_id = Country.objects.get(country='United States').id
#     # data = {'ticker': c.ticker, 'sic_code': c.industry.sic_code, 'country_id': country_id,
#     #         'sic_description': c.industry.sic_description, 'company_data': lll}
#     return JsonResponse(data)


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

    # print(1)

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

    # print(1000)

    return JsonResponse(dic)


# Admin
# load sic numbers from the SEC
# def set_sic_code(request):
#     acx = AcademyCityXBRL()
#     return acx.set_sic_code()

#
# def get_all_companies(request):
#     acx = AcademyCityXBRL()
#     dic = acx.get_all_companies()
#     return dic

def get_option_bf_detail_for_ticker(request):
    ticker_ = request.POST.get('ticker')
    dic = TDAmeriTrade().get_option_bf_detail_for_ticker(ticker=ticker_)
    # print(dic)
    return dic


def get_option_statistics_for_ticker(request):
    ticker_ = request.POST.get('ticker')
    dic = TDAmeriTrade().get_option_statistics_for_ticker(ticker=ticker_)
    # print(dic)
    return dic


def get_option_chain(request):
    ticker_ = request.POST.get('ticker')
    dic = TDAmeriTrade().get_option_chain(ticker=ticker_)
    # print(dic)
    return dic


def tdameritrade_setup_w_attribute(request):
    try:
        fun_ = request.POST.get('fun')
        attribute_ = request.POST.get('attribute')
        attribute_value_ = request.POST.get('attribute_value')
        # print(fun_)
        if attribute_ != "":
            print('TDAmeriTrade().' + fun_ + '('+attribute_+'="'+attribute_value_+'")')
            dic = eval('TDAmeriTrade().' + fun_ + '('+attribute_+'="'+attribute_value_+'")')
        else:
            dic = eval('TDAmeriTrade().' + fun_ + '()')
        # print(dic)
    except Exception as ex:
        # print(fun_ + '(request)')
        dic = eval(fun_+'(request)')
    return JsonResponse(dic)


def get_earning_forecast_sp500_view_main_detail(request):
    ticker_ = request.POST.get('ticker')
    # print('get_earning_forecast_sp500_view_main_')
    # print('order_by_')
    # print(order_by_)
    # print('order_by_')
    # print('order_by_')
    dic = AcademyCityXBRL().get_earning_forecast_sp500_view_main_detail(ticker=ticker_)
    # print('get_earning_forecast_sp500_view_main_1')
    # print(dic)
    # print('get_earning_forecast_sp500_view_main_2')
    return dic


def get_earning_forecast_sp500_view_main(request):
    order_by_ = request.POST.get('order_by')
    # print('get_earning_forecast_sp500_view_main_')
    # print('order_by_')
    # print(order_by_)
    # print('order_by_')
    # print('order_by_')
    dic = AcademyCityXBRL().get_earning_forecast_sp500_view_main(order_by=order_by_)
    # print('get_earning_forecast_sp500_view_main_1')
    # print(dic)
    # print('get_earning_forecast_sp500_view_main_2')
    return dic


def update_statistics(request):
    try:
        log_debug("Start update_statistics: " + datetime.datetime.now().strftime("%H:%M:%S"))
        for s in XBRLSPStatistics.objects.all():
            s.set_company_statistics(is_update=False)
        log_debug("End update_statistics " + datetime.datetime.now().strftime("%H:%M:%S"))
    except Exception as ex:
        print(ex)
    return {'status': 'ok'}


def analysis_setup_attribute(request):
    try:
        fun_ = request.POST.get('fun')
        attribute_ = request.POST.get('attribute')
        attribute_value_ = request.POST.get('attribute_value')
        # print(fun_, attribute_, attribute_value_)
        try:
            s_ = 'FinancialAnalysis().' + fun_ + '(request=request,'+attribute_+'="'+attribute_value_+'")'
            print(s_)
            dic = eval(s_)
        except Exception as ex:
            print("Error analysis_setup_attribute.")
        return JsonResponse(dic)

    except Exception as ex:
        return JsonResponse({'status': 'error: '+str(ex)})


def admin_setup_attribute(request):
    try:
        fun_ = request.POST.get('fun')
        attribute_ = request.POST.get('attribute')
        attribute_value_ = request.POST.get('attribute_value')
        # print(fun_)
        # print(attribute_)
        # print(attribute_value_)
        try:
            # print('AcademyCityXBRL().' + fun_ + '('+attribute_+'="'+attribute_value_+'")')
            dic = eval('AcademyCityXBRL().' + fun_ + '('+attribute_+'="'+attribute_value_+'")')
            # print(dic)
        except Exception as ex:
            dic = eval(fun_+'(request)')
        return JsonResponse(dic)

    except Exception as ex:
        return JsonResponse({'status': 'error: '+str(ex)})


def update_region_risk_premium(request):
    return AcademyCityXBRL().update_region_risk_premium(request)


def admin_setup(request):
    try:
        fun_ = request.POST.get('fun')
        try:
            # print('AcademyCityXBRL().' + fun_ + '()')
            dic = eval('AcademyCityXBRL().' + fun_ + '()')
            # print(dic)
        except Exception as ex:
            dic = eval(fun_+'(request)')
        return JsonResponse(dic)

    except Exception as ex:
        return JsonResponse({'status': 'error: '+str(ex)})

#
# def load_tax_rates_by_country_year(request):
#     try:
#         acx = AcademyCityXBRL()
#         dic = acx.load_tax_rates_by_country_year()
#         return dic
#     except Exception as ex:
#         return JsonResponse({'status': 'error: '+str(ex)})

#
# def load_sp_returns(request):
#     acx = AcademyCityXBRL()
#     dic = acx.load_sp_returns()
#     return dic


def load_country_premium(request):
    acx = AcademyCityXBRL()
    dic = acx.load_country_premium(request)
    return dic

# End Admin


# XBRL
def get_accounts(request):
    cik_ = 'aapl'  # '0000320193' # '0000051143'
    type_ = '10-K'
    accounting_principle_ = 'us-gaap'
    accounts_ = {'bs': {'stockholdersequity'}, 'is': {'revenuefromcontractwithcustomerexcludingassessedtax'}}
    acx = AcademyCityXBRL()

    # data = acx.get_data_for_cik(cik=cik_, type=type_, accounting_principle=accounting_principle_, accounts=accounts_)
    #
    # sp_tickers = acx.get_sp500()
    # print(sp_tickers)

    # all_companies = acx.get_all_companies()
    # print(all_companies)

    # accounts = acx.get_value(accounts_=accounts)
    # print('acx.get_value()')
    # print(accounts)
    # print('acx.get_value()')

    # data = acx.get_industries()

    return JsonResponse(data)


def delete_todo(request):
    pky_ = request.POST.get('pky')
    ToDoList.objects.filter(id=pky_).delete()
    dic = {'record': pky_}
    return JsonResponse(dic)


def update_todo(request):
    dic = {'status': 'ok'}
    id_ = request.POST.get('id')
    value_ = request.POST.get('value')
    # print(value_)

    if value_ == "false":
        value_ = False
    elif value_ == "true":
        value_ = True
    pky_ = request.POST.get('pky')

    try:
        if pky_ == '':
            c = ToDoList.objects.create()
        else:
            c = ToDoList.objects.get(id=pky_)
    except Exception as ex:
        print(ex)

    setattr(c, id_, value_)
    c.save()

    # print('getattr(c, id)')
    # print(getattr(c, "id"))

    dic["result"] = getattr(c, "id")
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


def update_data_year(request):
    # print('-1'*50)
    # print(1111)
    # print('-1'*50)
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

    # print('-1'*50)
    # print(22222)
    # print('-1'*50)

    wd = os.getcwd()
    sdata = wd + '/academycity/apps/corporatevaluation/data/'
    sr = sdata + str(nyear) + '.xlsx'

    # print('-'*100)
    # print(sr)
    # print('-'*100)

    df = pd.read_excel(sr, 'Data')

    # print(df)

    # nnn_ = 0


    # print('-1'*50)
    # print(333333)
    # print('-1'*50)

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
            # print('-1' * 50)
            # print(e)
            # print('-1' * 50)
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
    # print('---')
    # print(s_url)
    # print('---')

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


# SEC
def sec(request):
    # cik = '320193'
    # accession_number = '000032019320000096'
    # u = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='+cik+'&accession_number='+accession_number+'&xbrl_type=v#'
    #
    # headers = {'User-Agent': 'amos@drbaranes.com'}
    # edgar_resp = requests.get(u, headers=headers)
    # edgar_str = edgar_resp.text
    #
    # # print(edgar_str)
    #
    # m = re.search('new Array\((.+?)\)', edgar_str)
    # if m:
    #     last_r = m.group(1)
    # # print(last_r)
    #
    # soup = BeautifulSoup(edgar_str, 'html.parser')
    # table = str(soup.find('table'))
    # # print(table)

    return render(request, 'corporatevaluation/sec/sec.html', {})


def get_sec(request):
    # cik = request.POST.get('cik')
    # accession_number = request.POST.get('accession_number')
    # cik = '320193'
    # accession_number = '000032019320000096'
    # u = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='+cik+'&accession_number='+accession_number+'&xbrl_type=v#'

    u = request.POST.get('url')

    # print('u')
    # print(u)
    # print('u')

    headers = {'User-Agent': 'amos@drbaranes.com'}
    edgar_resp = requests.get(u, headers=headers)
    edgar_str = edgar_resp.text
    m = re.search('new Array\((.+?)\)', edgar_str)
    if m:
        last_r = m.group(1)
    soup = BeautifulSoup(edgar_str, 'html.parser')
    table = soup.find('table')
    table.find('tr').decompose()
    table.find('img').decompose()
    return JsonResponse({'table': str(table), 'last_r': last_r})


def get_r(request):
    url_r = request.POST.get('url_r')
    # url = 'https://www.sec.gov'+url_r
    headers = {'User-Agent': 'amos@drbaranes.com'}
    edgar_resp = requests.get(url_r, headers=headers)
    # print(edgar_resp.text)
    dic = {'html': edgar_resp.text}
    return JsonResponse(dic)

#
# def clean_data_for_all_companies(request):
#     acx = AcademyCityXBRL()
#     dic = acx.clean_data_for_all_companies()
#     return dic


def create_company_by_ticker(request):
    ticker = request.POST.get('ticker')
    # print('-1-'*10)
    # print(ticker)
    # print('-1-'*10)
    acx = AcademyCityXBRL()
    response = acx.create_company_by_ticker(ticker)
    return JsonResponse(response)

#
# def copy_processed_companies(request):
#     acx = AcademyCityXBRL()
#     dic = acx.copy_processed_companies()
#     return dic


def get_data_ticker(request):
    ticker_ = request.POST.get('ticker')
    # print(ticker_)
    is_update_ = request.POST.get('is_update')
    is_updateq_ = request.POST.get('is_updateq')
    # print(is_update_)
    project = Project.objects.filter(translations__language_code=get_language()).get(id=request.session['cv_project_id'])
    XBRLCountryYearData.project = project
    acx = AcademyCityXBRL()
    data = acx.get_data_ticker(ticker=ticker_, is_update=is_update_, is_updateq=is_updateq_)
    # print(data)
    # request.session['cv_statements'] = data['statements']
    return JsonResponse(data)


# Valuation
def get_risk_premium(request):
    year50 = request.POST.get('year50')
    year10 = request.POST.get('year10')
    cv_project_id = request.POST.get('cv_project_id')
    is_update = request.POST.get('is_update')
    acx = AcademyCityXBRL()
    data = acx.get_risk_premium(year10=year10, year50=year50, cv_project_id=cv_project_id, is_update=is_update)
    return JsonResponse(data)


# Data processing
def get_matching_accounts(request):
    ticker_ = request.POST.get('ticker')
    year_ = request.POST.get('year')
    sic_ = request.POST.get('sic')
    acx = AcademyCityXBRL()
    return JsonResponse(acx.get_matching_accounts(ticker=ticker_, year=year_, sic=sic_))


def onchange_account(request):
    # print('-1'*20)
    accounting_standard_ = request.POST.get('accounting_standard')
    match_account_ = request.POST.get('match_account')
    account_order = request.POST.get('account_order')
    ticker = request.POST.get('ticker')
    year_ = request.POST.get('year')
    sic_ = request.POST.get('sic')
    # print('-2'*20)
    company_ = XBRLCompanyInfo.objects.get(ticker=ticker)
    # print(company_)
    # print('-13'*20)

    # print('account_order')
    # print(account_order)
    if account_order != "-1":
        # print('account_id')
        account_ = XBRLValuationAccounts.objects.get(order=account_order)
        # print('account_')
        # print(account_)
        # print('account_')

    try:
        # print('-1'*10)
        # print('match_account_')
        # print(company_)
        # print(year_)
        # print(match_account_)
        # print(accounting_standard_)
        # print('match_account_')

        account_to_delete = XBRLValuationAccountsMatch.objects.get(year=year_, company=company_,
                                                                   match_account=match_account_,
                                                                   accounting_standard=accounting_standard_)
        account_to_delete.delete()

        # print('-11'*10)
    except Exception as ex:
        pass
        # print("error 101: " + str(ex))

    try:
        # print('-22'*10)
        if account_order != "-1":
            i, created = XBRLValuationAccountsMatch.objects.get_or_create(year=year_, company=company_, account=account_,
                                                                          match_account=match_account_,
                                                                          accounting_standard=accounting_standard_)
        # print('-21'*10)
        # print(i)
        # print('-22'*10)
        # print(created)
        # print('-23'*10)

        acx = AcademyCityXBRL()
        matching_accounts, accounts, used_accounting_standards = \
            acx.get_matching_accounts(ticker=ticker, year=int(year_), sic=sic_,
                                      statements=request.session['cv_statements'])

        dic = {'status': 'ok', 'matching_accounts': matching_accounts}

        # print('dic matching_accounts')
        # print(dic)
        # print('dic matching_accounts')
        return JsonResponse(dic)

    except Exception as ex:
        print("error 102: " + str(ex))
        dic = {'status': 'not ok'}

    # print('-2'*20)
    return JsonResponse(dic)


def save_industry_default(request):
    ticker_ = request.POST.get('ticker')
    year_ = request.POST.get('year')
    sic_ = request.POST.get('sic')
    acx = AcademyCityXBRL()
    dic = acx.save_industry_default(year=int(year_), ticker=ticker_, sic=sic_)
    return JsonResponse(dic)


def get_duplications_tickers(request):
    dic = {'status': 'ok'}
    for q in XBRLCompanyInfo.objects.values('ticker').annotate(count=Count('id')).values('ticker').order_by().filter(count__gt=1):
        # print('q')
        # print(q)
        # print('q')
        try:
            c = XBRLCompanyInfo.objects.filter((Q(exchange='nasdaq') | Q(exchange='amex')) & Q(ticker=q['ticker'])).all()[0]
        except Exception as ex:
            # print("Error 100: " + str(ex))
            try:
                c = XBRLCompanyInfo.objects.filter(Q(exchange='nyse') & Q(ticker=q['ticker'])).all()[0]
            except Exception as ex:
                print("Error 110: " + str(ex))
        # print(c)
        try:
            c.delete()
        except Exception as ex:
            print("Error 200: "+str(ex))
    # print(dic)
    return dic

#
# def test(request):
#     acx = AcademyCityXBRL()
#     return acx.test()

#
# def test1(request):
#     acx = AcademyCityXBRL()
#     acx.test1()
