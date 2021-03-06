# https://www.codeproject.com/Articles/1227268/Accessing-Financial-Reports-in-the-EDGAR-Database
# https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
from django.conf import settings
import pandas as pd
import string
import datetime
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
from six.moves import urllib
from django.db.models import Avg
from .models import (XBRLMainIndustryInfo, XBRLIndustryInfo, XBRLCompanyInfoInProcess,
                     XBRLCompanyInfo, XBRLValuationStatementsAccounts, XBRLValuationAccounts, XBRLValuationAccountsMatch,
                     XBRLRegion, XBRLCountry, XBRLCountryYearData,
                     XBRLHistoricalReturnsSP, XBRLSPMoodys)

# cik = '0000051143'
# type = '10-K'
# dateb = '20160101'


class AcademyCityXBRL(object):
    def __init__(self):
        self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", "corporatevaluation")
        os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)

        self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
        os.makedirs(self.TO_DATA_PATH, exist_ok=True)
        # print(self.TO_DATA_PATH)

        self.IMAGES_PATH = os.path.join(self.TO_DATA_PATH, "images")
        os.makedirs(self.IMAGES_PATH, exist_ok=True)
        # print(self.IMAGES_PATH)

        self.MODELS_PATH = os.path.join(self.TO_DATA_PATH, "models")
        os.makedirs(self.MODELS_PATH, exist_ok=True)
        # print(self.MODELS_PATH)

        self.EXCEL_PATH = os.path.join(self.TO_DATA_PATH, "excel")
        os.makedirs(self.EXCEL_PATH, exist_ok=True)
        # print(self.EXCEL_PATH)

        self.Data = None

        self.sp_tickers = []

        self.xbrl_base_year = 2020
        self.xbrl_start_year = 2012
        self.today_year = datetime.datetime.now().year

    # Valuation Functions
    def get_risk_premium(self, year10=1928, year50=1928):
        dic = {'Arithmetic': {}, 'Geometric': {}}
        try:
            l_years = [1928, year50, year10]
            for y in l_years:

                # print(y)
                # for rp in XBRLHistoricalReturnsSP.objects.filter(year__gte=y).all():
                #     try:
                #         print(rp)
                #         print(rp.return_on_sp500, rp.tb3ms_rate, rp.return_on_tbond)
                #     except Exception as ex:
                #         print(ex)
                #
                # print(2222222)
                ll = [[rp.return_on_sp500, rp.tb3ms_rate, rp.return_on_tbond] for rp in XBRLHistoricalReturnsSP.objects.filter(year__gte=y).all()]

                df = pd.DataFrame(ll)
                df.columns = ['M', 'TB', 'B']
                df['M_TB'] = df['M'] - df['TB']
                df['M_B'] = df['M'] - df['B']
                # print(df)
                # print(df.mean())
                # print(df.std())
                # print(df.std()/((df.shape[0]+1)**(1/2)))
                dic['Arithmetic'][y] = {}
                dic['Geometric'][y] = {}
                dic['Arithmetic'][y]['Stocks-TBills'] = {}
                dic['Arithmetic'][y]['Stocks-TBonds'] = {}
                dic['Geometric'][y]['Stocks-TBills'] = {}
                dic['Geometric'][y]['Stocks-TBonds'] = {}

                dic['Arithmetic'][y]['Stocks-TBills']['value'] = round(10000*df.mean()['M_TB'])/10000
                dic['Arithmetic'][y]['Stocks-TBills']['std'] = round(10000*df.std()['M_TB']/((df.shape[0]+1)**(1/2)))/10000
                dic['Arithmetic'][y]['Stocks-TBonds']['value'] = round(10000*df.mean()['M_B'])/10000
                dic['Arithmetic'][y]['Stocks-TBonds']['std'] = round(10000*df.std()['M_B']/((df.shape[0]+1)**(1/2)))/10000
                gm = 1
                gtb = 1
                gb = 1
                for i, r in df.iterrows():
                    gm *= (1+r['M'])
                    gtb *= (1+r['TB'])
                    gb *= (1+r['B'])
                gm = gm**(1/df.shape[0]) - 1
                gtb = gtb**(1/df.shape[0]) - 1
                gb = gb**(1/df.shape[0]) - 1
                dic['Geometric'][y]['Stocks-TBills']['value'] = round(10000*(gm - gtb))/10000
                dic['Geometric'][y]['Stocks-TBonds']['value'] = round(10000*(gm - gb))/10000
                dic['Geometric'][y]['Stocks-TBills']['std'] = ''
                dic['Geometric'][y]['Stocks-TBonds']['std'] = ''

            # print(dic)
        except Exception as ex:
            print(ex)
        return dic

    # Assisting functions
    def download_excel_file(self, url, file):
        path = os.path.join(self.EXCEL_PATH, file + ".xlsx")
        if not os.path.isfile(path):
            urllib.request.urlretrieve(url, path)
        return path

    def load_excel_data(self, file, sheet_name=None):
        excel_path = os.path.join(self.EXCEL_PATH, file + ".xlsx")
        if sheet_name:
            self.DATA = pd.read_excel(excel_path, engine='openpyxl', sheet_name=sheet_name)
        else:
            self.DATA = pd.read_excel(excel_path, engine='openpyxl')
        return self.DATA

    # I use ticker as cik
    def get_data_for_cik(self, cik, type='10-k'):
        dic_company_info = {'company_info': {'ticker': cik,
                                             'type': type,
                                             }
                            }
        headers = {'User-Agent': 'amos@drbaranes.com'}
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}"  # &dateb={}"
        url = base_url.format(cik, type)

        dic_company_info['company_info']['10k_url'] = url
        #
        # print('-'*100)
        # print(url)
        # print('-'*100)
        #
        # print("Current Time 1 =", datetime.datetime.now().strftime("%H:%M:%S"))
        edgar_resp = requests.get(url, headers=headers, timeout=30)
        # print("Current Time 11 =", datetime.datetime.now().strftime("%H:%M:%S"))
        edgar_str = edgar_resp.text
        #
        cik0 = ''
        cik_re = re.compile(r'.*CIK=(\d{10}).*')
        results = cik_re.findall(edgar_str)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            cik0 = str(results[0])
        dic_company_info['company_info']['CIK'] = cik0
        #
        sic0 = ''
        cik_re = re.compile(r'.*SIC=(\d{4}).*')
        results = cik_re.findall(edgar_str)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            sic0 = str(results[0])
        dic_company_info['company_info']['SIC'] = sic0
        #
        # Find the document links
        soup = BeautifulSoup(edgar_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile2')

        try:
            rows = table_tag.find_all('tr')
        except Exception as ex:
            return dic_company_info
        dic_data = {}
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) > 3:
                    if cells[0].text.lower() != type.lower():
                        continue
                    # for filing_year in range(2019, 2020):
                    for filing_year in range(self.xbrl_start_year, self.today_year+1):
                        if str(filing_year) in cells[3].text:
                            dic_data[filing_year] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
            except Exception as ex:
                pass
                # print(ex)

        # need to add send message on no data
        if len(dic_data) == 0:
            print("Couldn't find the document link")
            return dic_company_info

        # Obtain HTML for document page
        statements = {}
        for statement in XBRLValuationStatementsAccounts.objects.all():
            statements[statement.order] = {'name': statement.statement, 'accounts': {}}
            for a in statement.xbrl_valuation_statements.all():
                statements[statement.order]['accounts'][a.order] = [a.account, a.type, a.scale]
        #
        # print(statements)
        #
        dic_data_list = []
        for key, value in dic_data.items():
            temp = [key, value,
                    dic_company_info['company_info']['SIC'],
                    dic_company_info['company_info']['ticker'], statements
                    ]
            dic_data_list.append(temp)

        # Exit if document link couldn't be found
        # print('-13' * 10)
        # print(len(dic_data))
        # print(dic_company_info['company_info'])
        # print(dic_data)
        # print(dic_data_list)
        # print('-13' * 10)

        results = []
        # print("Current Time Before ThreadPoolExecutor =", datetime.datetime.now().strftime("%H:%M:%S"))

        with ThreadPoolExecutor(max_workers=len(dic_data)) as pool:
            results = pool.map(self.get_data_for_years, dic_data_list)
        # print("Current Time After ThreadPoolExecutor =", datetime.datetime.now().strftime("%H:%M:%S"))
        for r in results:
            dic_data[r[0]] = r[1]
            # statements = r[4]

        # print("Current Time After process result ThreadPoolExecutor =", datetime.datetime.now().strftime("%H:%M:%S"))

        dic_company_info['data'] = dic_data
        # acc['instant'].sort()
        # acc['flow'].sort()
        dic_company_info['statements'] = statements

        # print('-16' * 10)
        # print(dic_company_info)
        # print('-16' * 10)

        return dic_company_info

    def insure_two_digit_month_day(self, s):
        if len(s) == 1:
            s = "0"+s
        return s

    def get_data_for_years(self, dic_data_year):
        # print("Current Time Start get data = " + str(dic_data_year[0]), datetime.datetime.now().strftime("%H:%M:%S"))
        # dic_data_year[3] = ticker
        # dic_data_year[0] = year
        # dic_data_year[2] = sic

        # print('-30'*10)
        # print(str(dic_data_year[0]) + dic_data_year[1]['href'])
        # print('-30'*10)

        headers = {'User-Agent': 'amos@drbaranes.com'}
        try:
            # print("Current Time 2 =", datetime.datetime.now().strftime("%H:%M:%S"))
            doc_resp = requests.get(dic_data_year[1]['href'], headers=headers, timeout=30)
            # print("Current Time 21 =", datetime.datetime.now().strftime("%H:%M:%S"))
        except Exception as exc:
            print(exc)
            return dic_data_year

        doc_str = doc_resp.text

        # Find the XBRL link
        xbrl_link = ''
        soup = BeautifulSoup(doc_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')

        # print('-1-'*10)
        # print(dic_data_year[0])
        # print(dic_data_year[1]['href'])
        # print('-1-'*10)

        try:
            rows = table_tag.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 3:
                    if 'INS' in cells[3].text or 'XML' in cells[3].text:
                        #
                        # print(cells[3].text)
                        #
                        xbrl_link = cells[2].a['href']

            dic_data_year[1]['xbrl_link'] = 'https://www.sec.gov' + xbrl_link
            accession_number = xbrl_link.split('/')
            # print('-1'*10)
            # print(accession_number)
            # print('-1'*10)

            view_link = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='
            view_link += accession_number[4]+'&accession_number='+accession_number[5]+'&xbrl_type=v#'

            r_link = "https://www.sec.gov/Archives/edgar/data/"+accession_number[4]+"/"+accession_number[5]+"/R"

            dic_data_year[1]['r_link'] = r_link
            dic_data_year[1]['view_link'] = view_link
        except Exception as ex:
            return dic_data_year

        try:
            # print("Current Time 3 =", datetime.datetime.now().strftime("%H:%M:%S"))
            xbrl_resp = requests.get(dic_data_year[1]['xbrl_link'], headers=headers, timeout=30)
            # print("Current Time 31 =", datetime.datetime.now().strftime("%H:%M:%S"))
        except Exception as exc:
            print(exc)
            return dic_data_year

        xbrl_str = xbrl_resp.text
        # print("Current Time 32 =", datetime.datetime.now().strftime("%H:%M:%S"))
        soup = BeautifulSoup(xbrl_str, 'lxml')
        # print("Current Time 33 =", datetime.datetime.now().strftime("%H:%M:%S"))

        dic_data_year[1]['dei'] = {}
        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            dic_data_year[1]['dei'][name_[1]] = tag.text
        # print("Current Time 34 =", datetime.datetime.now().strftime("%H:%M:%S"))

        documentperiodenddate = dic_data_year[1]['dei']['documentperiodenddate']
        entitycentralindexkey = dic_data_year[1]['dei']['entitycentralindexkey']

        # print(documentperiodenddate)
        # print(entitycentralindexkey)

        # print("Current Time 4 =", datetime.datetime.now().strftime("%H:%M:%S"))
        for tag in soup.find_all(name=re.compile('enddate'), string=documentperiodenddate):
            # print(tag.name)
            try:
                context = tag.find_parent(re.compile('context'))
                # print(context)
                context_name = context.name.split(":")
                # print('=-3-'*50)
                # print(context.name + ' : ' + str(len(context_name)))
                # print('=-3-'*50)

                if len(context_name) > 1:
                    identifier = context.find(context_name[0] + ':identifier')
                    segment = context.find(context_name[0] +':segment')
                    startdate = context.find(context_name[0] +':startdate')
                else:
                    identifier = context.find('identifier')
                    segment = context.find('segment')
                    startdate = context.find('startdate')
                end_date = tag.text.split('-')
                start_date = startdate.text.split('-')
                start_date = start_date[0]+'-'+start_date[1]

                start_date_should = str((int(end_date[0])-1))+'-'+end_date[1]
                start_date1_should = end_date[0]+'-01'
                start_date2_should = str((int(end_date[0])-1))+'-'+self.insure_two_digit_month_day(str((int(end_date[1])+1)))
                start_date3_should = str((int(end_date[0])-1))+'-'+self.insure_two_digit_month_day(str((int(end_date[1])-1)))

                # print('-6'*10)
                # print('end_date')
                # print(end_date)
                # print('end_date')
                # print(start_date_should)
                # print(start_date1_should)
                # print(start_date2_should)
                # print(start_date)
                # print('=5'*10)
                # print('=6'*10)

                if (not segment) and (identifier.text == entitycentralindexkey) \
                        and (start_date == start_date_should or start_date == start_date1_should or start_date == start_date2_should or start_date == start_date3_should):
                    flow_context_id = context['id']

            except Exception as ex:
                # print(ex)
                continue

        # print('-flow'*20)
        # print(flow_context_id)
        # print(documentperiodenddate)
        # print('-flow'*20)

        # print('=bs'*50)
        # print("Current Time 5 =", datetime.datetime.now().strftime("%H:%M:%S"))
        for tag in soup.find_all(name=re.compile('instant'), string=documentperiodenddate):
            context = tag.find_parent(re.compile('context'))

            context_name = context.name.split(":")
            # print('=--'*50)
            # print(context.name + ' : ' + str(len(context_name)))
            # print('=--'*50)

            if len(context_name) > 1:
                identifier = context.find(context_name[0] + ':identifier')
                segment = context.find(context_name[0] +':segment')
            else:
                identifier = context.find('identifier')
                segment = context.find('segment')
            if not segment and identifier.text == entitycentralindexkey:
                # print(context)
                instant_context_id = context['id']

        # print('-instant'*10)
        # print(instant_context_id)
        # print(documentperiodenddate)
        # print('-instant'*10)

        matching_accounts, accounts_, used_accounting_standards = \
            self.get_matching_accounts(dic_data_year[3], int(dic_data_year[1]['dei']['documentfiscalyearfocus']),
                                       dic_data_year[2], dic_data_year[4])

        dic_data_year[1]['matching_accounts'] = matching_accounts
        year_data = {}

        # print("Current Time 6 =", datetime.datetime.now().strftime("%H:%M:%S"))
        for std in used_accounting_standards:
            tag_list = soup.find_all(re.compile(std+":"))
            for tag in tag_list:
                name_ = tag.name.split(":")
                try:
                    if name_[1] in accounts_['instant'] and tag['contextref'] == instant_context_id:
                        order = accounts_['instant'][name_[1]][0]
                        scale = accounts_['instant'][name_[1]][1]
                        if scale == 1:
                            year_data[order] = tag.text
                        else:
                            year_data[order] = int(tag.text)/scale

                    if name_[1] in accounts_['flow'] and tag['contextref'] == flow_context_id:
                        order = accounts_['flow'][name_[1]][0]
                        scale = accounts_['flow'][name_[1]][1]
                        if scale == 1:
                            year_data[order] = tag.text
                        else:
                            year_data[order] = int(tag.text)/scale

                except Exception as ex:
                    pass
                    # print("Error: year=" + str(dic_data_year[0]) + "   dic=" + dic_data_year[1]['href'] + "   " + str(ex) + tag.text)

        dic_data_year[1]['year_data'] = year_data
        # print("Current Time End get data = " + str(dic_data_year[0]), datetime.datetime.now().strftime("%H:%M:%S"))
        return dic_data_year

    def get_matching_accounts(self, ticker, year, sic, statements):
        try:
            if year <= self.xbrl_base_year:
                years = sorted(range(year, self.xbrl_base_year+1), reverse=True)
            else:
                years = range(self.xbrl_base_year, year+1)
        except Exception as ex:
            print(ex)

        matches = XBRLValuationAccountsMatch.objects.filter((Q(year=0) & Q(company__industry__sic_code=sic)) |
                                                            (Q(year__in=years) & Q(company__ticker=ticker))).all()
        used_accounting_standards = []
        dic_matches = {}
        for m in matches:
            if m.year == 0:
                dic_matches[m.account.order] = [m.match_account, m.accounting_standard]
                if m.accounting_standard not in used_accounting_standards:
                    used_accounting_standards.append(m.accounting_standard)
        for y in years:
            for m in matches:
                if m.year == y:
                    dic_matches[m.account.order] = [m.match_account, m.accounting_standard]
                    if m.accounting_standard not in used_accounting_standards:
                        used_accounting_standards.append(m.accounting_standard)

        # print('dic_matches')
        # print(dic_matches)
        # print('dic_matches')

        matching_accounts = {}
        accounts_ = {'instant': {}, 'flow': {}}

        for st_ in statements:
            for a_order in statements[st_]['accounts']:
                # statements[st_]['accounts'][a_order] = [a.account, a.type, a.scale]
                # dic_matches[a_order] = [m.match_account, m.accounting_standard]

                # print(a_order)
                # if int(a_order) in dic_matches:
                #     print('in')
                # else:
                #     print('not')
                # print('str')
                # print(dic_matches)
                # if str(a_order) in dic_matches:
                #     print('in')
                # else:
                #     print('not')
                # print('str')

                if int(a_order) in dic_matches:
                    ma_, ma_std = dic_matches[a_order][0].lower(), dic_matches[a_order][1].lower()
                else:
                    ma_, ma_std = "", ""

                # print(ma_)

                if ma_ != '':
                    if statements[st_]['accounts'][a_order][1] == 1:
                        accounts_['instant'][ma_] = (a_order, statements[st_]['accounts'][a_order][2])
                    else:
                        accounts_['flow'][ma_] = (a_order, statements[st_]['accounts'][a_order][2])
                matching_accounts[a_order] = [ma_, ma_std]
        return matching_accounts, accounts_, used_accounting_standards

    def save_industry_default(self, year, ticker, sic):
        dic = {'status': 'ok'}
        if year == self.xbrl_base_year:
            print('-1'*20)
            industry = XBRLIndustryInfo.objects.get(sic_code=sic)
            c, created = XBRLCompanyInfo.objects.get_or_create(industry=industry, company_name=sic, ticker=sic, cik=sic)
            try:
                print('-2'*20)
                # zero_company = XBRLValuationAccountsMatch.objects.filter(Q(company__ticker=ticker) & Q(year=year)).all()
                # zero_company.update(company=c, year=0)
                for m in XBRLValuationAccountsMatch.objects.filter(Q(company__ticker=ticker) & Q(year=year)).all():
                    cs, created_s = XBRLValuationAccountsMatch.objects.get_or_create(year=0,company=c,account=m.account)
                    if created_s:
                        cs.match_account = m.match_account
                        cs.accounting_standard = m.accounting_standard
                        cs.save()
                        m.delete()
            except Exception as ex:
                print('-3'*20)
                print(ex)
                dic = {'status': 'ko'}
        else:
            dic = {'status': 'You can update only data of year 2020.'}
        return dic

    def get_sp500(self):
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.sp_tickers = list(pd.read_html(sp500_url)[0]['Symbol'].values)
        return sp_tickers

    # # #
    def create_company_by_ticker(self, ticker=None):
        try:
            company_id = -1
            type = '10-k'
            #
            headers = {'User-Agent': 'amos@drbaranes.com'}
            base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}"  # &dateb={}"
            url = base_url.format(ticker, type)
            #
            # print('-'*100)
            # print(url)
            # print('-'*100)
            #
            edgar_resp = requests.get(url, headers=headers, timeout=30)
            edgar_str = edgar_resp.text
            #
            cik0 = ''
            cik_re = re.compile(r'.*CIK=(\d{10}).*')
            results = cik_re.findall(edgar_str)
            if len(results):
                results[0] = int(re.sub('\.[0]*', '.', results[0]))
                cik0 = str(results[0])
            # print('-1'*10)
            # print(cik0)
            # print('-1'*10)
            #
            sic0 = ''
            cik_re = re.compile(r'.*SIC=(\d{4}).*')
            results = cik_re.findall(edgar_str)
            if len(results):
                results[0] = int(re.sub('\.[0]*', '.', results[0]))
                sic0 = int(results[0])

            # print('-1'*10)
            # print(sic0)
            # print('-1'*10)

            soup = BeautifulSoup(edgar_str, 'html.parser')
            company_name_ = soup.find('span', class_='companyName').text
            company_name_n = company_name_.index("CIK#")
            company_name_ = company_name_[0:company_name_n]
            # print(company_name_)

            table_tag = soup.find('table', class_='tableFile2')
            rows = table_tag.find_all('tr')
            dic_data = {}
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) > 3:
                        # print(cells[3].text)
                        for filing_year in range(self.xbrl_start_year, self.today_year + 1):
                            if str(filing_year) in cells[3].text:
                                dic_data[filing_year] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
                except Exception as ex:
                    pass

            # print('len(dic_data)')
            # print(len(dic_data))

            if len(dic_data) > 0:
                industry_ = XBRLIndustryInfo.objects.get(sic_code=sic0)
                # print(industry_)
                # print(cik0)
                # print(sic0)
                # print(ticker)
                # print(company_name_)
                # print(company_name_[0].upper())

                company, created = XBRLCompanyInfo.objects.get_or_create(industry=industry_, ticker=ticker,cik=cik0,
                                                                         company_name=company_name_,
                                                                         company_letter=company_name_[0].upper())
                company_id = company.id

        except Exception as ex:
            print('error 1: '+str(ex))
        return {'status': 'ok', 'id': company_id, 'company_name': company_name_}

    def clean_data_for_all_companies(self):
        companies_ = XBRLCompanyInfoInProcess.objects.all()
        for company in companies_:
            ticker = company.ticker
            type = '10-k'
            try:
                #
                headers = {'User-Agent': 'amos@drbaranes.com'}
                base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}"  # &dateb={}"
                url = base_url.format(ticker, type)
                #
                # print('-'*100)
                # print(url)
                # print('-'*100)
                #
                edgar_resp = requests.get(url, headers=headers, timeout=30)
                edgar_str = edgar_resp.text
                #
                cik0 = ''
                cik_re = re.compile(r'.*CIK=(\d{10}).*')
                results = cik_re.findall(edgar_str)
                if len(results):
                    results[0] = int(re.sub('\.[0]*', '.', results[0]))
                    cik0 = str(results[0])
                # print('-1'*10)
                # print(cik0)
                # print('-1'*10)
                #
                sic0 = ''
                cik_re = re.compile(r'.*SIC=(\d{4}).*')
                results = cik_re.findall(edgar_str)
                if len(results):
                    results[0] = int(re.sub('\.[0]*', '.', results[0]))
                    sic0 = int(results[0])

                # print('-1'*10)
                # print(sic0)
                # print('-1'*10)

                company.cik = cik0
                company.sic = sic0
                company.save()
            except Exception as ex:
                # print('error 1: '+str(ex))
                company.is_error = True
                company.message = "Can not get CIK or SIC: " + str(ex)
                company.cik = ''
                company.sic = 0
                company.save()
                continue

            # print('-2'*10)
            #
            # Find the document links
            soup = BeautifulSoup(edgar_str, 'html.parser')
            table_tag = soup.find('table', class_='tableFile2')
            try:
                # print('-3'*10)
                rows = table_tag.find_all('tr')
                # print('-4'*10)

            except Exception as ex:
                # print('-5'*10)
                # print(str(ex))

                company.message = "there are no data rows: " + str(ex)
                # print('-51'*10)
                try:
                    company.save()
                except Exception as exc:
                    pass
                    # print('-52'*10)
                    # print(str(exc))
                # print('-6'*10)
                continue

            dic_data = {}
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) > 3:
                        # print(cells[3].text)
                        # for filing_year in range(2019, 2020):
                        for filing_year in range(self.xbrl_start_year, self.today_year+1):
                            if str(filing_year) in cells[3].text:
                                dic_data[filing_year] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
                except Exception as ex:
                    pass
                    # print(ex)

            # print('-8'*10)

            # need to add send message on no data
            if len(dic_data) == 0:
                company.message = "there are no data."
                company.save()
                continue

            # print(cik0)
            # print('--9--'*5)
            company.save()
            # print('--10--'*5)
        return {'status': 'ok'}

    def copy_processed_companies(self):
        companies_ = XBRLCompanyInfoInProcess.objects.filter(is_error=False).all()
        for c in companies_:
            try:
                print(c.ticker)
                i_ = XBRLIndustryInfo.objects.get(sic_code=c.sic)
                XBRLCompanyInfo.objects.get_or_create(industry=i_, exchange=c.exchange, company_name=c.company_name,
                                                      ticker=c.ticker, company_letter=c.company_letter, cik=c.cik)
            except Exception as exc:
                print(str(exc))

    def get_all_companies(self):
        exchanges = {
            'nyse': 'nyse/newyorkstockexchange',
            'nasdaq': 'nasdaq/nasdaq',
            'amex': 'amex/americanstockexchange'}

        # writer = pd.ExcelWriter(self.EXCEL_PATH+'/all_companies.xlsx', engine='xlsxwriter')
        n = 0
        companies = None
        for exchange in exchanges:
            print(exchange)
            url = 'https://www.advfn.com/'+exchanges[exchange]+'.asp?companies='
            df = self.get_companies_for_exchange(exchange=exchange, exchange_url=url)
            if n == 0:
                companies = df
                n += 1
            else:
                frames = [companies, df]
                companies = pd.concat(frames)
            # df.to_excel(writer, sheet_name=exchange)
            # Close the Pandas Excel writer and output the Excel file.
        try:
            XBRLCompanyInfoInProcess.truncate()
        except Exception as ex:
            print("Error 1:  " + str(ex))
        try:
            # print(companies)
            for i, c in companies.iterrows():
                # print(c)
                # print(c['exchange'])
                # print(c['name'])
                print(c['ticker'])
                # print(c['letter'])
                a, created = XBRLCompanyInfoInProcess.objects.get_or_create(exchange=c['exchange'],
                                                                            company_name=c['name'],
                                                                            ticker=c['ticker'],
                                                                            company_letter=c['letter'])
        except Exception as ex:
            print("Error 2:  " + str(ex))

        # self.companies.reset_index(drop=True, inplace=True)
        # self.companies.to_excel(writer, sheet_name='all')
        # writer.save()

        return self.companies

    def get_companies_for_exchange(self, exchange, exchange_url):
        companies = pd.DataFrame(columns=['exchange', 'name', 'ticker', 'letter'])
        company_name = []
        company_ticker = []
        company_letter = []
        letters = string.ascii_uppercase
        for letter in letters:
            company_name, company_ticker, company_letter = self.get_companies_for_letter(
                letter, exchange_url+letter, company_name, company_ticker, company_letter)
        companies['name'] = company_name
        companies['ticker'] = company_ticker
        companies['exchange'] = exchange
        companies['letter'] = company_letter
        companies = companies[companies['ticker'] != '']
        return companies

    def get_companies_for_letter(self, letter, url, company_name, company_ticker, company_letter):
        page = requests.get(url, timeout=30)
        soup = BeautifulSoup(page.text, 'html.parser')
        odd_rows = soup.find_all('tr', attrs={'class': 'ts0'})
        even_rows = soup.find_all('tr', attrs={'class': 'ts1'})
        for r in odd_rows:
            cs = r.find_all('td')
            company_name.append(cs[0].text.strip())
            company_ticker.append(cs[1].text.strip())
            company_letter.append(letter)
        for r in even_rows:
            cs = r.find_all('td')
            company_name.append(cs[0].text.strip())
            company_ticker.append(cs[1].text.strip())
            company_letter.append(letter)
        return company_name, company_ticker, company_letter

    def set_sic_code(self):
        url = 'https://en.wikipedia.org/wiki/Standard_Industrial_Classification'
        headers = {'User-Agent': 'amos@drbaranes.com'}
        page = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(page.text, 'html.parser')
        tables = soup.find_all('table')
        rows = tables[0].find_all('tr')
        z = 0
        for r in rows:
            if z == 0:
                z = 1
                continue
            cs = r.find_all('td')
            sic_code_ = int(cs[0].text.strip().split('-')[1])
            sic_description_ = cs[1].text.strip()
            XBRLMainIndustryInfo.objects.get_or_create(sic_code=sic_code_, sic_description=sic_description_)
        url = 'https://www.sec.gov/corpfin/division-of-corporation-finance-standard-industrial-classification-sic-code-list'
        page = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.find_all('tr')
        main_sics = XBRLMainIndustryInfo.objects.all()
        z = 0
        for r in rows:
            if z == 0:
                z = 1
                continue
            cs = r.find_all('td')
            # print(cs[0].text.strip() + ':' + cs[2].text.strip())

            sic_code_ = int(cs[0].text.strip())
            sic_description_ = cs[2].text.strip()
            main_sic_ = 1999
            for main_sic in main_sics:
                if sic_code_ < main_sic.sic_code:
                    main_sic_ = main_sic
                    break
            XBRLIndustryInfo.objects.get_or_create(sic_code=sic_code_, main_sic=main_sic_,
                                                   sic_description=sic_description_)
        return {'status': 'ok'}
    # # #

    def load_tax_rates_by_country_year(self):
        url = "https://files.taxfoundation.org/20210125115215/1980-2020-Corporate-Tax-Rates-Around-the-World.csv.xlsx"
        file = "world_taxes"
        self.download_excel_file(url, file)
        df = self.load_excel_data(file)

        XBRLCountryYearData.truncate()
        for i, r in df.iterrows():
            region, c = XBRLRegion.objects.get_or_create(name=r['continent'])
            oecd = True if int(r['oecd']) > 0 else False
            eu27 = True if int(r['eu27']) > 0 else False
            gseven = True if int(r['gseven']) > 0 else False
            gtwenty = True if int(r['gtwenty']) > 0 else False
            brics = True if int(r['brics']) > 0 else False

            try:
                country, c = XBRLCountry.objects.get_or_create(region=region, name=r['country'], iso_2=r['iso_2'],
                                                               iso_3=r['iso_3'], oecd=oecd, gseven=gseven, eu27=eu27,
                                                               gtwenty=gtwenty, brics=brics)
            except Exception as ex:
                print('Error 1: ' + ex)

            d, c = XBRLCountryYearData.objects.get_or_create(country=country, year=int(r['year']))

            if not pd.isna(r['rate']):
                d.tax_rate = round(r['rate'], 2)

            if not pd.isna(r['gdp']):
                d.gdp = round(r['gdp'], 5)

            try:
                d.save()
            except Exception as ex:
                print(ex)

    def load_sp_returns(self):
        # https://github.com/7astro7/full_fred
        file = 'histretSP'
        df = self.load_excel_data(file, 'Data')
        df = df.sort_values(by=['year'])
        spi = 1
        bbbi = 1
        n = 0
        XBRLHistoricalReturnsSP.truncate()
        for i, r in df.iterrows():
            try:
                year_data, c = XBRLHistoricalReturnsSP.objects.get_or_create(year=int(r['year']))
                if not pd.isna(r['AAA']):
                    year_data.aaa = r['AAA']
                if not pd.isna(r['BBB']):
                    year_data.bbb = r['BBB']
                if not pd.isna(r['TB3MS']):
                    year_data.tb3ms = r['TB3MS']
                if not pd.isna(r['TB10Y']):
                    year_data.tb10y = r['TB10Y']
                if not pd.isna(r['SP500']):
                    year_data.sp500 = r['SP500']
                if not pd.isna(r['DividendYield']):
                    year_data.dividend_yield = r['DividendYield']
                if not pd.isna(r['ReturnsOnRealEstate']):
                    year_data.return_on_real_estate = r['ReturnsOnRealEstate']
                if not pd.isna(r['HomePrices']):
                    year_data.home_prices = r['HomePrices']
                if not pd.isna(r['CPI']):
                    year_data.cpi = r['CPI']
            except Exception as ex:
                print('Error 1: ' + ex)

            try:
                year_data.save()
                # print(int(year_data.year))
                if int(year_data.year) >= 1928:
                    spi = spi * (1 + year_data.return_on_sp500)
                    bbbi = bbbi * (1 + year_data.return_on_tbond)
                    n += 1
                    # print(spi)
                    # print(bbbi)
                    # print(n)
                    spi_ = spi ** (1 / n)
                    bbbi_ = bbbi ** (1 / n)
                    # print(spi_)
                    # print(bbbi_)
                    r = spi_ - bbbi_
                    # print(r)
                    year_data.risk_premium = round(10000 * r) / 10000
                year_data.save()
            except Exception as ex:
                print('ex')
                print(ex)
                print('ex')

    def load_country_premium(self):
        # print('in object load_country_premium(request)')
        match = {'Czech Republic': 'Czechia',
                 'Moldova': 'Republic of Moldova',
                 'United Kingdom': 'United Kingdom of Great Britain and NorthernIreland',
                 'Jersey (States of)': 'Jersey',
                 'Guernsey (States of)': 'Guernsey',
                 'Bolivia': 'Bolivia(Plurinational State of)',
                 "C??te d'Ivoire": "Cote d'Ivoire",
                 'Democratic Republic of Congo': 'Democratic Republic of the Congo',
                 'Congo (Democratic Republic of)': 'Democratic Republic of the Congo',
                 'Korea': 'Republic of Korea',
                 'Bolivia(Plurinational State of)': 'Bolivia (Plurinational State of)',
                 'United Kingdom of Great Britain and NorthernIreland': 'United Kingdom of Great Britain and Northern Ireland'}
        file = "ctrypremJuly21"
        df = self.load_excel_data(file, sheet_name="Data1")
        # print(df[100:])
        name_list = [x for x in df['name'].unique() if str(x) != 'nan']
        # print(name_list)

        # for r in df:
        #     print(df[r])

        for r in name_list:
            # print(r)
            # print(df.loc[df['name'] == r])
            # print("------")
            z = 0
            for i, c in df.loc[df['name'] == r].iterrows():
                if z == 0:
                    # print(c['name'])
                    try:
                        region, created = XBRLRegion.objects.get_or_create(name=c['name'])
                        region.full_name = c['Region']
                        if created:
                            region.updated_adamodar = True
                        region.save()
                    except Exception as ex:
                        print('Errot 10: '+ str(ex))
                    z = 1
                try:
                    if c['Country'] in match:
                        s_country = match[c['Country']]
                    else:
                        s_country = c['Country']
                    # print('='*20)
                    # print(s_country)
                    # if c['Country'] == 'Czech Republic':
                    #     s_country = 'Czechia'
                    # elif c['Country'] == 'Moldova':
                    #     s_country = 'Republic of Moldova'
                    # elif c['Country'] == 'United Kingdom':
                    #     s_country = 'United Kingdom of Great Britain and NorthernIreland'
                    # elif c['Country'] == 'Jersey (States of)':
                    #     s_country = 'Jersey'
                    # elif c['Country'] == 'Guernsey (States of)':
                    #     s_country = 'Guernsey'
                    # elif c['Country'] == 'Bolivia':
                    #     s_country = 'Bolivia(Plurinational State of)'
                    # elif c['Country'] == "C??te d'Ivoire":
                    #     s_country = "Cote d'Ivoire"
                    # elif c['Country'] == "Democratic Republic of Congo":
                    #     s_country = "Democratic Republic of the Congo"
                    # elif c['Country'] == "Congo (Democratic Republic of)":
                    #     s_country = "Democratic Republic of the Congo"
                    # elif c['Country'] == "Korea":
                    #     s_country = "Republic of Korea"
                    # elif c['Country'] == "Bolivia(Plurinational State of)":
                    #     s_country = "Bolivia (Plurinational State of)"
                    # else:
                    #     s_country = c['Country']

                    if not XBRLCountry.objects.filter(name=s_country).all().count() > 0:
                        XBRLCountry.objects.create(region=region, name=s_country, updated_adamodar=True)
                        # print('created')
                        # print(c['Country'])
                    else:
                        country = XBRLCountry.objects.filter(name=s_country).all()[0]
                        country.region = region
                        country.updated_adamodar = True
                        country.save()
                        # print('updated')
                        # print(c['Country'])
                except Exception as ex:
                    print('Error 100: ' + str(ex))
        # try:
        #     XBRLCountryYearData.objects.all().update(sp_rating='', moodys_rating='')
        # except Exception as ex:
        #     print(ex)

        # print('--SP Moodys')
        for i, c in df.iterrows():
            s_country_ = 'Country1'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            # print('-'*50)
            # print(s_country)
            # print(c)
            try:
                country = XBRLCountry.objects.filter(name=s_country).all()[0]
                data, created = XBRLCountryYearData.objects.get_or_create(country=country, year=2020)
                if str(c['sp_rating_2020']) == 'nan':
                    s_sp = ''
                else:
                    s_sp = c['sp_rating_2020']
                data.sp_rating = s_sp
                # print(s_country + "                  " + str(c['Moodys_rating_2020']))

                if str(c['Moodys_rating_2020']) == 'nan':
                    s_moodys = ''
                else:
                    s_moodys = c['Moodys_rating_2020']
                data.moodys_rating = s_moodys

                data.tax_rate = c['tax_rate_2020']
                data.save()
                # print(data)
            except Exception as ex:
                pass
                # print("Error 229: "+str(ex))
                # print(s_country)
                # print(c)
                # print("Error 229: "+str(ex))

        # print('--composite_risk_rating_7_21 --')
        for i, c in df.iterrows():
            s_country_ = 'Country2'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            # print(s_country)
            # print(c)

            try:
                country = XBRLCountry.objects.filter(name=s_country).all()[0]
                data, created = XBRLCountryYearData.objects.get_or_create(country=country, year=2020)
                data.composite_risk_rating = c['composite_risk_rating_7_21']
                data.save()
                # print(data)
            except Exception as ex:
                pass
                # print("Error 230: "+str(ex))
                # print(s_country)
                # print("Error 230: "+str(ex))

        # print('-- CDS_07_01_20211 --')
        for i, c in df.iterrows():
            s_country_ = 'Country3'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            # print(s_country)
            # print(c)
            try:
                data, created = XBRLCountryYearData.objects.get_or_create(country=country, year=2020)

                # need to consider this.  Since three country with missing data turned to 0.
                if str(c['CDS_01_01_2021']) == 'nan':
                    s_ = 0
                else:
                    s_ = 100*c['CDS_01_01_2021']
                data.cds = s_
                data.save()
                # print(data)
            except Exception as ex:
                pass
                # print("Error 231: "+str(ex))
                # print(s_country)
                # print("Error 231: "+str(ex))

        # print('-- SPMoodys 1--')
        for i, c in df.iterrows():
            try:
                # print('-'*50)
                # print(c['SP'])
                # print(c['Moodys'])
                # print(c['sp_moodys_year'])

                if str(c['sp_moodys_year']) != 'nan':
                    # print('-'*50)
                    # print(c['sp_moodys_year'])
                    d, created = XBRLSPMoodys.objects.get_or_create(year=c['sp_moodys_year'], sp=c['SP'], moodys=c['Moodys'])
                    # print(d)
            except Exception as ex:
                pass
                # print("Error 232: "+str(ex))
                # print(c['sp_moodys_year'])
                # print("Error 232: "+str(ex))

        # print('-- SPMoodys 2--')
        for i, c in df.iterrows():
            try:
                if str(c['Rating']) != 'nan':
                    d = XBRLSPMoodys.objects.get(year=int(c['rating_year']), moodys=c['Rating'])
                    dd = round(c['Default_Spread_1_1_2021']/100, 2)
                    d.default_spread = dd
                    d.save()
            except Exception as ex:
                pass
                # print("Error 233: "+str(ex))

        # print('Done')
