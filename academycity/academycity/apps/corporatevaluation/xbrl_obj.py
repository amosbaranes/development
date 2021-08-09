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
import xml.etree.ElementTree as ET
from .models import (XBRLMainIndustryInfo, XBRLIndustryInfo)


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
        self.companies = None

    # I use ticker as cik
    def get_data_for_cik(self, cik, type='10-k', accounting_principle='us-gaap', accounts=None):
        today_year = datetime.datetime.now().year
        dic_company_info = {'company_info': {'ticker': cik,
                                             'type': type,
                                             'accounting_principle': accounting_principle
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
        rows = table_tag.find_all('tr')
        dic_data = {}
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) > 3:
                    # print(cells[3].text)
                    for filing_year in range(2009, today_year+1):
                        if str(filing_year) in cells[3].text:
                            dic_data[filing_year] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
            except Exception as ex:
                pass
                # print(ex)

        # Exit if document link couldn't be found

        # print('-13'*10)
        # print(len(dic_data))
        # print('-13'*10)

        if len(dic_data) == 0:
            print("Couldn't find the document link")
            sys.exit()

        # Obtain HTML for document page

        acc = {'is': [], 'bs': []}
        for year in dic_data:
            try:
                dic_data[year]['dei'] = {}

                # print('-30'*10)
                # print(dic_data[year]['href'])
                # print('-30'*10)

                doc_resp = requests.get(dic_data[year]['href'], headers=headers)
                doc_str = doc_resp.text

                # print('-14' * 10)
                # print(99)
                # print('-14'*10)

                # Find the XBRL link
                xbrl_link = ''
                soup = BeautifulSoup(doc_str, 'html.parser')
                table_tag = soup.find('table', class_='tableFile', summary='Data Files')
                rows = table_tag.find_all('tr')
                for row in rows:
                    # print(row)
                    cells = row.find_all('td')
                    if len(cells) > 3:
                        if 'INS' in cells[3].text or 'XML' in cells[3].text:
                            #
                            # print(cells[3].text)
                            #
                            xbrl_link = cells[2].a['href']

                dic_data[year]['xbrl_link'] = 'https://www.sec.gov' + xbrl_link
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

                dic_data[year]['r_link'] = r_link
                dic_data[year]['view_link'] = view_link

                xbrl_resp = requests.get(dic_data[year]['xbrl_link'], headers=headers)
                xbrl_str = xbrl_resp.text
                soup = BeautifulSoup(xbrl_str, 'lxml')

                # print('-'*100)
                # print(dic_data[year]['xbrl_link'])
                # print('-'*100)

                for tag in soup.find_all(re.compile("dei:")):
                    name_ = tag.name.split(":")
                    dic_data[year]['dei'][name_[1]] = tag.text

                documentperiodenddate = dic_data[year]['dei']['documentperiodenddate']
                entitycentralindexkey = dic_data[year]['dei']['entitycentralindexkey']

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
                        else:
                            identifier = context.find('identifier')
                            segment = context.find('segment')
                        # print('=4'* 10)
                        # print(context)
                        # print('=4' * 10)
                        end_date = tag.text.split('-')
                        start_date = context.period.startdate.text.split('-')
                        start_date = start_date[0]+'-'+start_date[1]

                        # print('=5'*10)
                        # print(end_date[0])
                        # print((int(end_date[0])-1))
                        # print(str((int(end_date[0])-1)))

                        start_date_should = str((int(end_date[0])-1))+'-'+end_date[1]
                        start_date1_should = end_date[0]+'-01'
                        # print(start_date1_should)
                        # print('=5'*10)
                        # print(segment)
                        # print(identifier.text)
                        # print(entitycentralindexkey)
                        # print(start_date)
                        # print(start_date_should)
                        # print(start_date1_should)

                        # print('=6'*10)

                        if (not segment) and (identifier.text == entitycentralindexkey) \
                                and (start_date == start_date_should or start_date == start_date1_should):
                            # print('---context----')
                            # print(context)
                            # print('----context----')
                            is_context_id = context['id']

                    except Exception as ex:
                        # print(ex)
                        continue

                # print('-is'*50)
                # print(is_context_id)
                # print('-is'*50)

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
                    # print('=' * 10)
                    # print(context)
                    # print('=' * 10)
                    if not segment and identifier.text == entitycentralindexkey:
                        # print(context)
                        bs_context_id = context['id']

                # print('-bs2'*100)
                # print(bs_context_id)
                # print(documentperiodenddate)
                # print('-bs'*100)

                tag_list = soup.find_all(re.compile(accounting_principle+":"))
                year_data = {}
                for tag in tag_list:
                    name_ = tag.name.split(":")
                    if (name_[1] in accounts['bs'] and tag['contextref'] == bs_context_id) or \
                            (name_[1] in accounts['is'] and tag['contextref'] == is_context_id):
                        year_data[name_[1]] = tag.text
                    try:
                        if tag['contextref'] == bs_context_id and name_[1] not in acc['bs']:
                            acc['bs'].append(name_[1])
                        elif tag['contextref'] == is_context_id and name_[1] not in acc['is']:
                            acc['is'].append(name_[1])

                    except Exception as ex:
                        pass
                        # print(ex)

                dic_data[year]['year_data'] = year_data
                # print(acc)
            except Exception as ex:
                pass
                # print(ex)

        # print('20000000000000000000000022222222222222222')
        dic_company_info['data'] = dic_data
        acc['bs'].sort()
        acc['is'].sort()
        dic_company_info['accounts'] = acc
        # print(dic_company_info)
        return dic_company_info

    def get_sp500(self):
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.sp_tickers = list(pd.read_html(sp500_url)[0]['Symbol'].values)
        return sp_tickers

    def get_all_companies(self):
        exchanges = {'nyse': 'nyse/newyorkstockexchange',
                     'nasdaq': 'nasdaq/nasdaq',
                     'amex': 'amex/americanstockexchange'}
        writer = pd.ExcelWriter(self.EXCEL_PATH+'/all_companies.xlsx', engine='xlsxwriter')
        n = 0
        for exchange in exchanges:
            print(exchange)
            url = 'https://www.advfn.com/'+exchanges[exchange]+'.asp?companies='
            df = self.get_companies_for_exchange(exchange=exchange, exchange_url=url)
            if n == 0:
                self.companies = df
                n += 1
            else:
                frames = [self.companies, df]
                self.companies = pd.concat(frames)
            df.to_excel(writer, sheet_name=exchange)
            # Close the Pandas Excel writer and output the Excel file.
        self.companies.reset_index(drop=True, inplace=True)
        self.companies.to_excel(writer, sheet_name='all')
        writer.save()

        return self.companies

    def get_companies_for_exchange(self, exchange, exchange_url):
        companies = pd.DataFrame(columns=['exchange', 'company_name', 'company_ticker'])
        company_name = []
        company_ticker = []
        letters = string.ascii_uppercase
        for letter in letters:
            company_name, company_ticker = self.get_companies_for_letter(exchange_url+letter, company_name, company_ticker)
        companies['company_name'] = company_name
        companies['company_ticker'] = company_ticker
        companies['exchange'] = exchange
        companies = companies[companies['company_name'] != '']
        return companies

    def get_companies_for_letter(self, url, company_name, company_ticker):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        odd_rows = soup.find_all('tr', attrs={'class': 'ts0'})
        even_rows = soup.find_all('tr', attrs={'class': 'ts1'})
        for r in odd_rows:
            cs = r.find_all('td')
            company_name.append(cs[0].text.strip())
            company_ticker.append(cs[1].text.strip())
        for r in even_rows:
            cs = r.find_all('td')
            company_name.append(cs[0].text.strip())
            company_ticker.append(cs[1].text.strip())
        return company_name, company_ticker

    def get_industries_sic_code(self):
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

