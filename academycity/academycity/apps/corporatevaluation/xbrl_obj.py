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
from .models import (XBRLMainIndustryInfo, XBRLIndustryInfo, XBRLCompanyInfoInProcess,
                     XBRLCompanyInfo, XBRLValuationAccounts, XBRLValuationAccountsMatch)


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

        self.sp_tickers = []

        self.xbrl_base_year = 2020
        self.xbrl_start_year = 2012

    # I use ticker as cik
    def get_data_for_cik(self, cik, type='10-k', accounting_standard='us-gaap'):
        today_year = datetime.datetime.now().year
        dic_company_info = {'company_info': {'ticker': cik,
                                             'type': type,
                                             'accounting_standard': accounting_standard
                                             }
                            }
        headers = {'User-Agent': 'amos@drbaranes.com'}
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}"  # &dateb={}"
        url = base_url.format(cik, type)

        dic_company_info['company_info']['10k_url'] = url
        #
        print('-'*100)
        print(url)
        print('-'*100)
        #
        edgar_resp = requests.get(url, headers=headers)
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
        dic_company_info['company_info']['CIK'] = cik0
        #
        sic0 = ''
        cik_re = re.compile(r'.*SIC=(\d{4}).*')
        results = cik_re.findall(edgar_str)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            sic0 = str(results[0])
        # print('-2'*10)
        # print(sic0)
        # print('-12'*10)
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
                    # print(cells[3].text)
                    # for filing_year in range(2019, 2020):
                    for filing_year in range(self.xbrl_start_year, today_year+1):
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
        acc = {'flow': [], 'instant': []}
        #
        dic_data_list = []
        for key, value in dic_data.items():
            temp = [key, value,
                    dic_company_info['company_info']['SIC'],
                    dic_company_info['company_info']['ticker'],
                    acc, accounting_standard]
            dic_data_list.append(temp)

        # Exit if document link couldn't be found
        # print('-13' * 10)
        # print(len(dic_data))
        # print(dic_company_info['company_info'])
        # print(dic_data)
        # print(dic_data_list)
        # print('-13' * 10)

        results = []
        with ThreadPoolExecutor(max_workers=len(dic_data)) as pool:
            results = pool.map(self.get_data_for_years, dic_data_list)
        for r in results:
            dic_data[r[0]] = r[1]
            acc = r[4]

        dic_company_info['data'] = dic_data
        acc['instant'].sort()
        acc['flow'].sort()
        dic_company_info['accounts'] = acc

        # print('-16' * 10)
        print(dic_company_info)
        # print('-16' * 10)

        return dic_company_info

    def get_matching_accounts(self, ticker, year, sic):
        try:
            if year <= self.xbrl_base_year:
                years = sorted(range(year, self.xbrl_base_year+1), reverse=True)
            else:
                years = range(self.xbrl_base_year, year+1)
        except Exception as ex:
            print(ex)

        matches = XBRLValuationAccountsMatch.objects.filter((Q(year=0) & Q(company__industry__sic_code=sic)) |
                                                            (Q(year__in=years) & Q(company__ticker=ticker))).all()
        dic_matches = {}
        for m in matches:
            if m.year == 0:
                dic_matches[m.account.id] = m.match_account

        # print('dic_matches 1')
        # print(dic_matches)
        # print('dic_matches 10')
        for y in years:
            for m in matches:
                if m.year == y:
                    dic_matches[m.account.id] = m.match_account

        matches_for_report = {}
        accounts_ = {'instant': [], 'flow': []}
        accounts__ = XBRLValuationAccounts.objects.order_by("order").all()
        for a in accounts__:
            # print(str(a.id)+"--"+str(a.order)+"--"+a.account )
            try:
                if a.id in dic_matches:
                    ma_ = dic_matches[a.id]
                else:
                    ma_ = ""
                matches_for_report[a.order] = [a.account, ma_, a.id, a.type]

                if a.type == 1:
                    accounts_['instant'].append(ma_.lower())
                else:
                    accounts_['flow'].append(ma_.lower())

            except Exception as ex:
                print('ex')
                print(str(ex))
                print('ex')
        return matches_for_report, accounts_

    def insure_two_digit_month_day(self, s):
        if len(s) == 1:
            s = "0"+s
        return s

    def get_data_for_years(self, dic_data_year):
        # dic_data_year[3] = ticker
        # dic_data_year[0] = year
        # dic_data_year[2] = sic
        dic_data_year[1]['dei'] = {}

        # print('-30'*10)
        # print(str(dic_data_year[0]) + dic_data_year[1]['href'])
        # print('-30'*10)

        headers = {'User-Agent': 'amos@drbaranes.com'}
        doc_resp = requests.get(dic_data_year[1]['href'], headers=headers)
        doc_str = doc_resp.text

        # Find the XBRL link
        xbrl_link = ''
        soup = BeautifulSoup(doc_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')

        # print('-1-'*10)
        # print('-1-'*10)
        # print(dic_data_year[0])
        # print(dic_data_year[1]['href'])
        # print('-1-'*10)
        # print('-1-'*10)

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

        # print('r_link')
        # print(r_link)
        # print('r_link')

        dic_data_year[1]['r_link'] = r_link
        dic_data_year[1]['view_link'] = view_link

        xbrl_resp = requests.get(dic_data_year[1]['xbrl_link'], headers=headers)
        xbrl_str = xbrl_resp.text
        soup = BeautifulSoup(xbrl_str, 'lxml')

        # print('-'*100)
        # print(dic_data[year]['xbrl_link'])
        # print('-'*100)

        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            dic_data_year[1]['dei'][name_[1]] = tag.text

        documentperiodenddate = dic_data_year[1]['dei']['documentperiodenddate']
        entitycentralindexkey = dic_data_year[1]['dei']['entitycentralindexkey']

        # print(documentperiodenddate)
        # print(entitycentralindexkey)

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
        # print('-flow'*20)

        # print('=bs'*50)
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

        matching_accounts, accounts_ = self.get_matching_accounts(dic_data_year[3], int(dic_data_year[1]['dei']['documentfiscalyearfocus']), dic_data_year[2])
        dic_data_year[1]['matching_accounts'] = matching_accounts

        tag_list = soup.find_all(re.compile(dic_data_year[5]+":"))
        year_data = {}
        for tag in tag_list:
            name_ = tag.name.split(":")
            try:
                # if name_[1] in accounts_['instant'] and tag['contextref'] == instant_context_id:
                #     print(name_[1])
                #     print(accounts_['instant'])

                if (name_[1] in accounts_['instant'] and tag['contextref'] == instant_context_id) or \
                        (name_[1] in accounts_['flow'] and tag['contextref'] == flow_context_id):
                    year_data[name_[1]] = tag.text
            except Exception as ex:
                print("Error: " + str(dic_data_year[0]) + "   " + dic_data_year[1]['href'] + "   " + str(ex))

            try:
                if tag['contextref'] == instant_context_id and name_[1] not in dic_data_year[4]['instant']:
                    dic_data_year[4]['instant'].append(name_[1])
                elif tag['contextref'] == flow_context_id and name_[1] not in dic_data_year[4]['flow']:
                    dic_data_year[4]['flow'].append(name_[1])
            except Exception as ex:
                pass
                # print(ex)

        dic_data_year[1]['year_data'] = year_data

        # print('year_data')
        # print(accounts)
        # print(("-"+str(year))*5)
        # print(year_data)
        # print(("-"+str(year))*5)
        # print('acc--'*10)
        # print(acc)

        return dic_data_year

    def save_industry_default(self, year, ticker, sic):
        dic = {'status': 'ok'}
        if year == self.xbrl_base_year:
            print('-1'*20)
            industry = XBRLIndustryInfo.objects.get(sic_code=sic)
            c, created = XBRLCompanyInfo.objects.get_or_create(industry=industry, company_name=sic, ticker=sic, cik=sic)
            try:
                print('-2'*20)
                zero_company = XBRLValuationAccountsMatch.objects.filter(company__ticker=ticker).all()
                zero_company.update(company=c, year=0)
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

    def clean_data_for_all_companies(self):
        companies_ = XBRLCompanyInfoInProcess.objects.all()
        for company in companies_:
            ticker = company.ticker
            type = '10-k'
            accounting_standard = 'us-gaap'
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
                edgar_resp = requests.get(url, headers=headers)
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
                        for filing_year in range(self.xbrl_start_year, today_year+1):
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
        page = requests.get(url)
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
        page = requests.get(url, headers=headers)
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
        page = requests.get(url, headers=headers)
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


