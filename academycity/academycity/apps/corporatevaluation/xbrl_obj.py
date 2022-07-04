# https://www.codeproject.com/Articles/1227268/Accessing-Financial-Reports-in-the-EDGAR-Database
# https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python

from bs4 import BeautifulSoup
import re
import os
from django.conf import settings
import pandas as pd
import string
import datetime
import time
from datetime import timedelta
from django.db.models import Q

from six.moves import urllib
import xlrd
import numpy as np
import statistics
from django.utils.translation import get_language
import math
from django.utils.dateparse import parse_date
import json
import asyncio
import requests
import aiohttp
import random
from tda import auth, client, orders
from tda.orders.common import Duration, Session

from channels.db import database_sync_to_async

from channels.layers import get_channel_layer

# import yfinance as yf
from yahoofinancials import YahooFinancials
from ..core.utils import log_debug, clear_log_debug
from ..core.sql import SQL
from ..core.models import Debug
from ..core.OptionsAmeriTrade import BaseTDAmeriTrade

from .models import (XBRLMainIndustryInfo, XBRLIndustryInfo, XBRLCompanyInfoInProcess,
                     XBRLCompanyInfo, XBRLValuationStatementsAccounts, XBRLValuationAccounts,
                     XBRLValuationAccountsMatch,
                     XBRLCountry, XBRLCountryYearData,
                     XBRLHistoricalReturnsSP, XBRLSPMoodys, Project,
                     XBRLRegion, XBRLRegionYearData, XBRLSPEarningForecast, XBRLSPStatistics,
                     XBRLDimTime, XBRLDimCompany, XBRLDimAccount, XBRLFactCompany,
                     XBRLRealEquityPrices, XBRLRealEquityPricesArchive)


# cik = '0000051143'
# type = '10-K'
# dateb = '20160101'

# https://github.com/alexgolec/tda-api


class GetAllUrlsProcessed(object):
    def __init__(self):
        self.name = 'GetAllUrlsProcessed'
        self.session = None
        self.agent = 'amos@drbaranes.com'

    async def get_page(self, url):
        headers = {'User-Agent': self.agent}
        async with self.session.get(url, headers=headers, timeout=30) as r:
            return await r.text()

    async def get_all_pages(self, urls, func, dic):
        tasks = []
        for url in urls:
            txt = await self.get_page(url)
            task = asyncio.create_task(func(self, txt, url, dic))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    async def process_all_pages(self, urls, func, dic):
        async with aiohttp.ClientSession() as session:
            self.session = session
            return await self.get_all_pages(urls, func, dic)


class TDAmeriTrade(BaseTDAmeriTrade):
    def __init__(self):
        super().__init__()
        self.client = None
        self.get_client()
        self.dic_share_prices = {}

    def get_client(self):
        try:
            self.client = auth.client_from_token_file(self.token_path + "/token", self.api_key)
        except Exception as fex:
            print(fex)
            try:
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                    try:
                        self.client = auth.client_from_login_flow(driver, self.api_key, self.callback_url,
                                                                  self.token_path + "/token")
                    except Exception as ex:
                        print(ex)
            except Exception as eex:
                print(eex)
        return self.client

    # ------ Queue example Should be removed --
    def run_stream_options_data(self, dic):
        asyncio.run(self.stream_options_data())

    async def worker(self, name, queue):
        l = []
        while True:
            # Get a "work item" out of the queue.
            k_ = await queue.get()
            sleep_for = k_["sleep_for"]
            n = str(k_["n"])
            l.append(n)
            # Sleep for the "sleep_for" seconds.
            await asyncio.sleep(sleep_for)

            # Notify the queue that the "work item" has been processed.
            queue.task_done()
            print(f'{n}-{name} has slept for {sleep_for:.2f} seconds')
        return l

    async def stream_options_data(self):
        # Create a queue that we will use to store our "workload".
        queue = asyncio.Queue()

        # Generate random timings and put them into the queue.
        total_sleep_time = 0
        for _ in range(20):
            sleep_for = random.uniform(0.05, 1.0)
            total_sleep_time += sleep_for
            queue.put_nowait({"n": _, "sleep_for": sleep_for})

        # Create three worker tasks to process the queue concurrently.
        tasks = []
        for i in range(3):
            task = asyncio.create_task(self.worker(f'worker-{i}', queue))
            tasks.append(task)

        # Wait until the queue is fully processed.
        started_at = time.monotonic()
        await queue.join()
        total_slept_for = time.monotonic() - started_at

        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.
        ll = await asyncio.gather(*tasks, return_exceptions=True)
        print(ll)
        print('====')
        print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
        print(f'total expected sleep time: {total_sleep_time:.2f} seconds')
    # ----------------------------------------

    def set_sp500_dic(self):
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.sp_tickers = list(pd.read_html(sp500_url)[0]['Symbol'].values)
        self.sp_tickers_list = [x.split('.')[0] for x in self.sp_tickers]
        self.sp_tickers_str = ""
        n_ = 0
        for ticker in self.sp_tickers:
            if n_ == 0:
                self.sp_tickers_str = ticker
                n_ += 1
            else:
                self.sp_tickers_str += ","+ticker
        # print(self.sp_tickers_str)
        return self.sp_tickers_str

    def update_options_statistics(self):
        log_debug("Start update_options_statistics: " + datetime.datetime.now().strftime("%H:%M:%S"))
        # print("Start update_options_statistics: " + datetime.datetime.now().strftime("%H:%M:%S"))
        start_date_ = datetime.datetime.now().date()
        end_date_ = (datetime.datetime.now() + datetime.timedelta(days=6)).date()
        # print(s.company.ticker, start_date_, end_date_)
        n = 0
        for s in XBRLSPStatistics.objects.all():
            try:
                n += 1
                if n % 100 == 0:
                    time.sleep(1)
                # print("-1"*50)
                # print(s.company.ticker)
                dic = self.get_option_chain(ticker=s.company.ticker, start_date=start_date_, end_date=end_date_)
                if dic['status'] == "ok":
                    try:
                        s.straddle_price = dic['straddle_price']
                        s.butterfly_price = dic['llc'][1]
                        s.save()
                        # log_debug("options DATA saved for: " + s.company.ticker)
                    except Exception as ex:
                        # log_debug("Error saving options for: " + s.company.ticker)
                        pass
                else:
                    # log_debug("Error getting options data for: " + s.company.ticker)
                    pass
            except Exception as ex:
                # print("error 202 save update_options_statistics: " + str(ex))
                # log_debug("Error 202 getting data 202 td: : " + str(ex) + " " + s.company.ticker)
                pass
        # print('end options')
        log_debug("End update_options_statistics: " + datetime.datetime.now().strftime("%H:%M:%S"))
        return {'status': 'ok'}

    def get_option_chain_new(self, ticker=None, start_date=None, end_date=None):
        # print("-1" * 50)
        # print("start td.get_option_chain for " + ticker)
        dic = {'status': 'ko'}
        try:
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    strike_range=self.client.Options.StrikeRange.IN_THE_MONEY,
                                                    from_date=start_date, to_date=end_date,
                                                    strategy=self.client.Options.Strategy.STRADDLE)
        except Exception as ex:
            print("Error in get_option_chain api options pull for : " + ticker)
            log_debug("Error in get_option_chain api options pull for : " + ticker)
            return dic

        # print('------options_---- ' + ticker)
        if len(options_['"putExpDateMap']) > 0 or len(options_['"callExpDateMap']) > 0:
            print(json.dumps(options_.json(), indent=4))
        # print('-----')

        return

        llp = []
        try:
            for d in options_.json()['putExpDateMap']:
                for p in options_.json()['putExpDateMap'][d]:
                    p_ = options_.json()['putExpDateMap'][d][p][0]
                    p_p = (p_['bid'] + p_['ask']) / 2
                    # print(d, p, p_p, p_['bid'], p_['ask'])
                    llp.append(p_p)
        except Exception as ex:
            return dic

        llc = []
        try:
            for d in options_.json()['callExpDateMap']:
                for c in options_.json()['callExpDateMap'][d]:
                    c_ = options_.json()['callExpDateMap'][d][c][0]
                    c_p = (c_['bid'] + c_['ask']) / 2
                    # print(d, c, c_p, c_['bid'], c_['ask'])
                    llc.append(c_p)
        except Exception as ex:
            return dic

        # print('td.get_option_chain 123')
        # print('llp')
        # print('---')
        # print(llp)
        # print('llc')
        # print('---')
        # print(llc)
        # print('---')
        # print('td.get_option_chain 124')
        # print('---')
        straddle_price = round(100 * (llp[2] + llc[2])) / 100
        butterfly_c = round(100 * (-2 * llc[2] + llc[1] + llc[3])) / 100
        butterfly_p = round(100 * (-2 * llp[2] + llp[1] + llp[3])) / 100
        dic = {'status': 'ok', 'straddle_price': straddle_price, "butterfly_c": butterfly_c, "butterfly_p": butterfly_p,
               'llc': llc, 'llp': llp}
        # log_debug("End get_option_chain: " + ticker)
        return dic

    def get_butterfly_price(self, strike_num, strikes, llc, llp):
        p0 = llc['calls']['date']['strikes'][strikes[strike_num]]["price"]
        pl = llc['calls']['date']['strikes'][strikes[strike_num - 1]]["price"]
        pr = llc['calls']['date']['strikes'][strikes[strike_num + 1]]["price"]
        bfc = round(100 * (-2 * p0 + pl + pr)) / 100
        p0 = llp['puts']['date']['strikes'][strikes[strike_num]]["price"]
        pl = llp['puts']['date']['strikes'][strikes[strike_num - 1]]["price"]
        pr = llp['puts']['date']['strikes'][strikes[strike_num + 1]]["price"]
        bfp = round(100 * (-2 * p0 + pl + pr)) / 100
        return bfc, bfp

    def get_complete_option_chain(self, ticker=None, start_date=None, end_date=None):
        print("start td.get_option_chain for 111 " + ticker)
        if not start_date:
            start_date = datetime.datetime.now().date()
            end_date = (datetime.datetime.now() + datetime.timedelta(days=360)).date()
        dic = {'status': 'ko'}
        try:
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    strike_count=5, from_date=start_date, to_date=end_date)
        except Exception as ex:
            print("Error 3456 in get_option_chain api options pull for : " + ticker + str(ex))
            return dic
        # print('------options_----')
        # print(json.dumps(options_.json(), indent=4))
        # print(123)
        try:
            llp = {'puts': {"dates": {}}}
            for d_ in options_.json()['putExpDateMap']:
                d = d_.split(":")[0]
                llp['puts']['dates'][d] = {}
                for p in options_.json()['putExpDateMap'][d_]:
                    p_ = options_.json()['putExpDateMap'][d_][p][0]
                    p_p = round(100*(p_['bid'] + p_['ask']) / 2)/100
                    llp['puts']['dates'][d][p] = {"price":p_p, "symbol":p_['symbol']}
        except Exception as ex:
            print("puts: " + str(ex))
            return dic
        # print(llp)
        # print(1234)
        try:
            llc = {'calls': {"dates": {}}}
            for d_ in options_.json()['callExpDateMap']:
                d = d_.split(":")[0]
                llc['calls']['dates'][d] = {}
                for c in options_.json()['callExpDateMap'][d_]:
                    c_ = options_.json()['callExpDateMap'][d_][c][0]
                    c_p = round(100 * (c_['bid'] + c_['ask']) / 2) / 100
                    llc['calls']['dates'][d][c] = {"price": c_p, "symbol": c_['symbol']}

        except Exception as ex:
            print("calls: " + str(ex))
            return dic
        # print(llc)
        # print(12345)
        pstrikes = []
        for d in llp['puts']['dates']:
            for k in llp['puts']['dates'][d]:
                if k not in pstrikes:
                    pstrikes.append(k)
        cstrikes = []
        for d in llc['calls']['dates']:
            for k in llc['calls']['dates'][d]:
                if k not in cstrikes:
                    cstrikes.append(k)
        # print(123456)
        try:
            #
            dic = '{"ticker": "' + ticker + '"}'
            price_data = self.get_quote(dic)['data'][ticker]
            # print(1234567)
            share_price = (price_data['bidPrice'] + price_data['askPrice']) / 2
            # print(share_price)
            # print(12345678)
            dic = {'status': 'ok', 'share_price': share_price, 'pstrikes': pstrikes, 'cstrikes': cstrikes,
                   'llc': llc, 'llp': llp}
            print(123456789)
            print(dic)

            print(1234567891)
        except Exception as ex:
            dic = {'status': 'ko'}
        return dic

    def get_option_chain_vertical(self, ticker=None, start_date=None, end_date=None):
        pass

    def get_option_chain(self, ticker=None, start_date=None, end_date=None):
        # print("start td.get_option_chain for 111 " + ticker)
        if not start_date:
            n_ = 6
            if ticker in ["SPY", "QQQ", "IWM"]:
                n_ = 2
                nday = datetime.datetime.today().weekday()  # Monday = 0
                if nday in [0, 2, 4]:
                    n_ = 1
                elif nday in [1, 3, 6]:
                    n_ = 2
                else:
                    n_ = 3
            start_date = datetime.datetime.now().date()
            end_date = (datetime.datetime.now() + datetime.timedelta(days=n_)).date()
        dic = {'status': 'ko'}
        # print('-'*20)
        # print("in get_option_chain api options pull for : " + ticker)
        # print('-'*20)
        try:
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    strike_count=5, from_date=start_date, to_date=end_date)
        except Exception as ex:
            # print("Error 3456 in get_option_chain api options pull for : " + ticker + str(ex))
            return dic
        # print('------options_----')
        # print(json.dumps(options_.json(), indent=4))
        # print(123)
        try:
            llp = {'puts': {}}
            for d_ in options_.json()['putExpDateMap']:
                # print("="*100)
                # print(d_)
                # print("="*100)
                d = d_.split(":")[0]
                llp['puts']['date'] = {'date': d}
                llp['puts']['date']['strikes'] = {}
                for p in options_.json()['putExpDateMap'][d_]:
                    p_ = options_.json()['putExpDateMap'][d_][p][0]
                    p_p = (p_['bid'] + p_['ask']) / 2
                    symbol = p_['symbol']
                    llp['puts']['date']['strikes'][p] = {"price": round(100 * p_p) / 100, "symbol": symbol}
        except Exception as ex:
            # print("puts: " + str(ex))
            return dic
        # print(1234)
        # print(llp)
        try:
            llc = {'calls': {}}
            for d_ in options_.json()['callExpDateMap']:
                d = d_.split(":")[0]
                llc['calls']['date'] = {'date': d}
                llc['calls']['date']['strikes'] = {}
                for c in options_.json()['callExpDateMap'][d_]:
                    c_ = options_.json()['callExpDateMap'][d_][c][0]
                    c_p = (c_['bid'] + c_['ask']) / 2
                    symbol = c_['symbol']
                    llc['calls']['date']['strikes'][c] = {"price": round(100 * c_p) / 100, "symbol": symbol}
        except Exception as ex:
            # print("calls: " + str(ex))
            return dic
        strikes = []
        for k in llp['puts']['date']['strikes']:
            if k not in strikes:
                strikes.append(k)
        for k in llc['calls']['date']['strikes']:
            if k not in strikes:
                strikes.append(k)
        # print(12345)
        try:
            straddle_price = round(100 * (llp['puts']['date']['strikes'][strikes[2]]["price"] +
                                          llc['calls']['date']['strikes'][strikes[2]]["price"])) / 100
            bfcl, bfpl = self.get_butterfly_price(strike_num=1, strikes=strikes, llc=llc, llp=llp)
            bfc0, bfp0 = self.get_butterfly_price(strike_num=2, strikes=strikes, llc=llc, llp=llp)
            bfcr, bfpr = self.get_butterfly_price(strike_num=3, strikes=strikes, llc=llc, llp=llp)
            llc_ = [bfcl, bfc0, bfcr]
            llp_ = [bfpl, bfp0, bfpr]
            #
            dic = '{"ticker": "' + ticker + '"}'
            price_data = self.get_quote(dic)['data'][ticker]
            # print(price_data)
            share_price = round(100*(price_data['bidPrice'] + price_data['askPrice']) / 2)/100
            # print(price_data['bidPrice'], price_data['askPrice'], price)

            # self.get_quote(ticker="GOOG"):
            dic = {'status': 'ok', 'ticker': ticker, 'share_price': share_price, 'straddle_price': straddle_price, 'strikes': strikes,
                   "llc_": llc_, "llp_": llp_, 'llc': llc, 'llp': llp}
            # log_debug("End get_option_chain: " + ticker)
            # print('-3'*100)
            # print(dic)
            # print('-3'*100)
        except Exception as ex:
            dic = {'status': 'ko'}
        # print(dic)
        return dic

    # Not used to be deleted --
    # pull data for all strikes of contract for type=(put or call)
    def get_option_strategy_lh_(self, options_, dic, option_type, l_=0.1, h_=0.9, ticker=""):
        # print(option_type)
        # print(ticker)
        # print(dic)
        try:
            for d in options_.json()[option_type + 'ExpDateMap']:
                # print(d)
                if 'date' not in dic:
                    dic['date'] = str(d).split(":")[0]
                    dic['tickers'] = {}
                elif dic['date'] != str(d).split(":")[0]:
                    dic['ticker'] = ticker
                    dic['underlyingPrice'] = options_.json()['underlyingPrice']
                    dic['date'] = str(d).split(":")[0]
                    dic['tickers'] = {}
                for t in options_.json()[option_type + 'ExpDateMap'][d]:
                    # print(options_.json()[option_type+'ExpDateMap'][d][t][0]['delta'])
                    if options_.json()[option_type + 'ExpDateMap'][d][t][0]['delta'] != "NaN":
                        if l_ < abs(options_.json()[option_type + 'ExpDateMap'][d][t][0]['delta']) < h_:
                            if t not in dic['tickers']:
                                dic['tickers'][t] = {}
                            dic['tickers'][t][option_type] = {}
                            dic['tickers'][t][option_type]['price'] = round(100 * (
                                        options_.json()[option_type + 'ExpDateMap'][d][t][0]['bid'] +
                                        options_.json()[option_type + 'ExpDateMap'][d][t][0]['ask']) / 2) / 100
                            dic['tickers'][t][option_type]['delta'] = round(
                                100 * options_.json()[option_type + 'ExpDateMap'][d][t][0]['delta']) / 100
                            dic['tickers'][t][option_type]['theta'] = round(
                                100 * options_.json()[option_type + 'ExpDateMap'][d][t][0]['theta']) / 100
                            dic['tickers'][t][option_type]['symbol'] = options_.json()[option_type + 'ExpDateMap'][d][t][0]['symbol']
                            # print(options_.json()[option_type+'ExpDateMap'][d][t][0])
        except Exception as ex:
            log_debug("Error 201 in get_option_chain api options pull for : " + ticker + " = " + str(ex))
            # print("Error 201 in get_option_chain api options pull for : " + ticker + " = " + str(ex))
        # print("in get_option_statistics_for_ticker 211 : for options: " + option_type)
        return dic

    def get_option_statistics_for_ticker(self, ticker):
        dic = {'status': 'ko'}
        # ticker = "^SPX" ticker = "^GSPC" print("="*100)
        n_ = 6
        if ticker in ["SPY", "QQQ", "IWM"]:
            n_ = 2
            nday = datetime.datetime.today().weekday()  # Monday = 0
            if nday in [0, 2, 4]:
                n_ = 1
            elif nday in [1, 3, 6]:
                n_ = 2
            else:
                n_ = 3
        # print("nday=", n_, "ticker=", ticker)
        try:
            start_date_ = datetime.datetime.now().date()
            end_date_ = (datetime.datetime.now() + datetime.timedelta(days=n_)).date()
            # print(start_date_, end_date_)
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    from_date=start_date_, to_date=end_date_)
        except Exception as ex:
            log_debug("Error 2345 in get_option_chain api options pull for : " + ticker + " = " + str(ex))
            return dic
        return {'status': 'ok', 'option_data_ticker': options_.json()}

    def get_prices(self, dic):
        # print(dic)
        dic = eval(dic)
        # print(dic)
        ticker_ = dic['ticker']
        r = self.client.get_price_history(ticker_,
                                          period_type=client.Client.PriceHistory.PeriodType.DAY,
                                          period=client.Client.PriceHistory.Period.ONE_DAY,
                                          frequency_type=client.Client.PriceHistory.FrequencyType.MINUTE,
                                          frequency=client.Client.PriceHistory.Frequency.EVERY_MINUTE)
        assert r.status_code == 200, r.raise_for_status()
        # print(json.dumps(r.json(), indent=4))
        dic = {'data': r}
        # print(dic)
        log_debug("End get_prices.")
        return dic

    def get_quote(self, dic):
        dic = eval(dic)
        ticker_ = dic['ticker']
        url = r"https://api.tdameritrade.com/v1/marketdata/{}/quotes".format(ticker_.upper())
        # print(url)
        pay_load = {'apikey': self.customer_key + '@AMER.OAUTHAP'}
        # print(pay_load)
        try:
            r = requests.get(url=url, params=pay_load).json()
            # print(r)
        except Exception as ex:
            print(ex)
        return {'data': r}

    def get_iron_condor(self, rdic):
        ticker = rdic['ticker']
        try:
            log_debug("Start ICondor for: " + ticker)
            rdic['is_success'] = False
            start_date_ = datetime.datetime.now().date()
            end_date_ = (datetime.datetime.now() + datetime.timedelta(days=6)).date()
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    from_date=start_date_, to_date=end_date_)
            # print('options_.json()')
            # print(options_.json())
            dicd = {}
            dicd = self.get_option_strategy_lh_(options_=options_, dic=dicd, option_type='call', l_=0.1, h_=0.4)
            # print(dicd)
            delta_call_low = -1
            strike_call_low = -1
            price_call_low = -1
            delta_put_high = -1
            strike_put_high = -1
            price_put_high = -1
            d_ = -1
            sk = -1
            sk1 = -1
            try:
                for k in dicd['tickers']:
                    if sk == -1:
                        sk = float(k)
                    else:
                        sk1 = float(k)
                        d_ = abs(sk1 - sk)
                        sk = sk1
                    delta_ = dicd['tickers'][k]['call']['delta']
                    price_ = dicd['tickers'][k]['call']['price']
                    if 0.3 >= delta_ >= 0.2:
                        if delta_ > delta_call_low:
                            delta_call_low = delta_
                            strike_call_low = k
                            price_call_low = price_
            except Exception as ex:
                log_debug(str(ex)+ " 1 " + ticker)
                return rdic
            try:
                strike_call_high = str(float(strike_call_low) + d_)
                if float(strike_call_low) < rdic['p']:
                    log_debug("float(strike_call_low) < rdic['p'] "+ticker)
                    return rdic
                delta_call_high = dicd['tickers'][strike_call_high]['call']['delta']
                price_call_high = dicd['tickers'][strike_call_high]['call']['price']
                dicd = {}
                dicd = self.get_option_strategy_lh_(options_=options_, dic=dicd, option_type='put', l_=0.1, h_=0.4)
            except Exception as ex:
                log_debug(str(ex) + " 2 " + ticker)
                return rdic
            try:
                for k in dicd['tickers']:
                    delta_ = abs(dicd['tickers'][k]['put']['delta'])
                    price_ = dicd['tickers'][k]['put']['price']
                    if 0.3 >= delta_ >= 0.2:
                        if delta_ > delta_put_high:
                            delta_put_high = delta_
                            strike_put_high = k
                            price_put_high = price_
            except Exception as ex:
                log_debug(str(ex) + " 3 " + ticker)
                return rdic
            # print(delta_put_high, strike_put_high, price_put_high, d_)
            if delta_put_high == -1:
                log_debug("delta_put_high == -1")
                return rdic
            try:
                strike_put_low = str(float(strike_put_high) - d_)
                # print(strike_put_low)
                delta_put_low = abs(dicd['tickers'][strike_put_low]['put']['delta'])
                price_put_low = dicd['tickers'][strike_put_low]['put']['price']
                # print(delta_put_low, strike_put_low, price_put_low, d_)
            except Exception as ex:
                log_debug(str(ex) + " 4 " + ticker)
                return rdic
            if delta_put_low == -1:
                log_debug("delta_put_low == -1")
                return rdic
            try:
                condor_price = round(100 * (price_call_low - price_call_high + price_put_high - price_put_low)) / 100
                result = {'call': {'low': {'delta': delta_call_low, 'strike': strike_call_low, 'price': price_call_low},
                                   'high': {'delta': delta_call_high, 'strike': strike_call_high,
                                            'price': price_call_high}},
                          'put': {'low': {'delta': delta_put_low, 'strike': strike_put_low, 'price': price_put_low},
                                  'high': {'delta': delta_put_high, 'strike': strike_put_high, 'price': price_put_high}}}
                rdic['condor_price'] = condor_price
                rdic['condor'] = result
                rdic['is_success'] = True
            except Exception as ex:
                log_debug(str(ex) + " 5 " + ticker)
                return rdic
            # print(rdic)
        except Exception as ex:
            print("Error 7891 in get_option_chain api options pull for : " + str(ex) + " " + ticker)
            return rdic
        # print('End -5000  ' + ticker)
        return rdic

    def get_quotes(self, dic):
        # print(dic)
        # print(type(dic))
        dic = eval(dic)
        ticker_ = dic['ticker']
        #
        # need to pull the list of all stocks
        list1 = "SPX,RUT,IWM,QQQ,NDX,SPY,TSLAS,PYPL,AMZN,BABA,FB" # "MMM,ABT,ABBV,ABMD,ACN,ATVI,ADBE"

        if ticker_ == "ALL":
            ticker_ = list1

        # print(self.sp_tickers_str)
        log_debug("get_quotes: " + ticker_)
        url = r"https://api.tdameritrade.com/v1/marketdata/quotes"
        pay_load = {'apikey': self.customer_key + "@AMER.OAUTHAP", 'symbol': ticker_}
        # print(pay_load)
        r = requests.get(url=url, params=pay_load)
        data = r.json()
        # print(data)
        log_debug("get_quotes 100: data pulled")
        results = {}
        for k in data:
            # print(k)
            log_debug("Start ticker: "+k)
            d = datetime.datetime.fromtimestamp(data[k]['quoteTimeInLong'] / 999.999451)
            m = d.minute
            h = d.hour
            date_ = d.date()
            dic_k = {"ticker": k, "date": str(date_), "h": h, "m": m, "p": data[k]['lastPrice']}
            result = self.get_iron_condor(dic_k)
            if result['is_success']:
                # print('result')
                # print(result)
                cld = result['condor']['call']['low']['delta']
                cls = float(result['condor']['call']['low']['strike'])
                clp = result['condor']['call']['low']['price']
                chd = result['condor']['call']['high']['delta']
                chs = float(result['condor']['call']['high']['strike'])
                chp = result['condor']['call']['high']['price']

                pld = result['condor']['put']['low']['delta']
                pls = float(result['condor']['put']['low']['strike'])
                plp = result['condor']['put']['low']['price']

                phd = result['condor']['put']['high']['delta']
                phs = float(result['condor']['put']['high']['strike'])
                php = result['condor']['put']['high']['price']

                ep = round(100*((clp - chp) + (php - plp)))/100
                elc = round(100*((chs - cls) * (cld - chd) / 2 + chd * (chs - cls)))/100
                elp = round(100*((phs - pls) * (phd - pld) / 2 + pld * (phs - pls)))/100
                # print(ep, elc, elp)
                # print('-' * 100)
                result['expected_profit'] = ep - elc - elp
                results[k] = result
            else:
                continue

        dic = {'data': results}
        # print(dic)
        # print("End get_Quotes.")
        return dic

    # ------
    async def get_iron_condora(self, rdic):
        ticker = rdic['ticker']
        try:
            rdic['is_success'] = False
            start_date_ = datetime.datetime.now().date()
            end_date_ = (datetime.datetime.now() + datetime.timedelta(days=6)).date()
            options_ = self.client.get_option_chain(ticker, contract_type=self.client.Options.ContractType.ALL,
                                                    from_date=start_date_, to_date=end_date_)
            # print('options_.json()')
            # print(options_.json())
            dicd = {}
            dicd = self.get_option_strategy_lh_(options_=options_, dic=dicd, option_type='call', l_=0.1, h_=0.4)
            # print(dicd)
            delta_call_low = -1
            strike_call_low = -1
            price_call_low = -1
            delta_put_high = -1
            strike_put_high = -1
            price_put_high = -1
            d_ = -1
            sk = -1
            sk1 = -1
            try:
                for k in dicd['tickers']:
                    if sk == -1:
                        sk = float(k)
                    else:
                        sk1 = float(k)
                        d_ = abs(sk1 - sk)
                        sk = sk1
                    delta_ = dicd['tickers'][k]['call']['delta']
                    price_ = dicd['tickers'][k]['call']['price']
                    if 0.3 >= delta_ >= 0.2:
                        if delta_ > delta_call_low:
                            delta_call_low = delta_
                            strike_call_low = k
                            price_call_low = price_
            except Exception as ex:
                return rdic
            try:
                strike_call_high = str(float(strike_call_low) + d_)
                if float(strike_call_low) < rdic['p']:
                    return rdic
                delta_call_high = dicd['tickers'][strike_call_high]['call']['delta']
                price_call_high = dicd['tickers'][strike_call_high]['call']['price']
                dicd = {}
                dicd = self.get_option_strategy_lh_(options_=options_, dic=dicd, option_type='put', l_=0.1, h_=0.4)
            except Exception as ex:
                return rdic
            try:
                for k in dicd['tickers']:
                    delta_ = abs(dicd['tickers'][k]['put']['delta'])
                    price_ = dicd['tickers'][k]['put']['price']
                    if 0.3 >= delta_ >= 0.2:
                        if delta_ > delta_put_high:
                            delta_put_high = delta_
                            strike_put_high = k
                            price_put_high = price_
            except Exception as ex:
                return rdic
            # print(delta_put_high, strike_put_high, price_put_high, d_)
            if delta_put_high == -1:
                return rdic
            try:
                strike_put_low = str(float(strike_put_high) - d_)
                # print(strike_put_low)
                delta_put_low = abs(dicd['tickers'][strike_put_low]['put']['delta'])
                price_put_low = dicd['tickers'][strike_put_low]['put']['price']
                # print(delta_put_low, strike_put_low, price_put_low, d_)
            except Exception as ex:
                return rdic
            if delta_put_low == -1:
                return rdic
            try:
                condor_price = round(100 * (price_call_low - price_call_high + price_put_high - price_put_low)) / 100
                result = {'call': {'low': {'delta': delta_call_low, 'strike': strike_call_low, 'price': price_call_low},
                                   'high': {'delta': delta_call_high, 'strike': strike_call_high,
                                            'price': price_call_high}},
                          'put': {'low': {'delta': delta_put_low, 'strike': strike_put_low, 'price': price_put_low},
                                  'high': {'delta': delta_put_high, 'strike': strike_put_high, 'price': price_put_high}}}
                rdic['condor_price'] = condor_price
                rdic['condor'] = result
                rdic['is_success'] = True
            except Exception as ex:
                return rdic
        except Exception as ex:
            print("Error 7891 in get_option_chain api options pull for : " + str(ex) + " " + ticker)
            return rdic
        return rdic

    async def get_quotesa(self, i):
        # print(dic)
        # print(type(dic))
        ticker_ = self.get_tickers(i)
        #
        print(ticker_)

        url = r"https://api.tdameritrade.com/v1/marketdata/quotes"
        pay_load = {'apikey': self.customer_key + "@AMER.OAUTHAP", 'symbol': ticker_}
        url = url+"?apikey="+self.customer_key+"@AMER.OAUTHAP&symbol="+ticker_
        async with aiohttp.ClientSession as session:
            r = await aiohttp.get(url=url, params=pay_load)

        data = await r.json()
        # print(json.dumps(data))

        for k in data:
            print(k)
            d = datetime.datetime.fromtimestamp(data[k]['quoteTimeInLong'] / 999.999451)
            m = d.minute
            h = d.hour
            date_ = d.date()
            dic_k = {"ticker": k, "date": str(date_), "h": h, "m": m, "p": data[k]['lastPrice']}
            try:
                print(datetime.datetime.now().strftime("%H:%M:%S"))
                result = await self.get_iron_condora(dic_k)
                print(datetime.datetime.now().strftime("%H:%M:%S"))
                print(result['is_success'])
            except Exception as ex:
                print(str(ex))
            if result['is_success']:
                # print('result')
                # print(result)
                cld = result['condor']['call']['low']['delta']
                cls = float(result['condor']['call']['low']['strike'])
                clp = result['condor']['call']['low']['price']
                chd = result['condor']['call']['high']['delta']
                chs = float(result['condor']['call']['high']['strike'])
                chp = result['condor']['call']['high']['price']

                pld = result['condor']['put']['low']['delta']
                pls = float(result['condor']['put']['low']['strike'])
                plp = result['condor']['put']['low']['price']

                phd = result['condor']['put']['high']['delta']
                phs = float(result['condor']['put']['high']['strike'])
                php = result['condor']['put']['high']['price']

                ep = round(100*((clp - chp) + (php - plp)))/100
                elc = round(100*((chs - cls) * (cld - chd) / 2 + chd * (chs - cls)))/100
                elp = round(100*((phs - pls) * (phd - pld) / 2 + pld * (phs - pls)))/100
                # print(ep, elc, elp)
                # print('-' * 100)
                result['expected_profit'] = ep - elc - elp
                print(json.dumps(result))
            else:
                continue
        # print("End get_Quotes.")
        return dic

    def get_tickers(self, i):
        n = 1
        k_ = self.sp_tickers_list[i*n: (i+1)*n]
        k = ""
        n_ = 0
        for ticker in k_:
            if n_ == 0:
                k = ticker
                n_ += 1
            else:
                k += ","+ticker
        return k

    def run_stream_options_dataa(self):
        asyncio.run(self.stream_options_dataa())

    async def workera(self, name, queue):
        while True:
            # Get a "work item" out of the queue.
            k_ = await queue.get()
            queue.task_done()
            n = str(k_["n"])
            await self.get_quotesa(int(n))

            # Notify the queue that the "work item" has been processed.
            # print(f'{n}-{name} has slept for {sleep_for:.2f} seconds')

    async def stream_options_dataa(self):
        # Create a queue that we will use to store our "workload".
        queue = asyncio.Queue()

        # Generate random timings and put them into the queue.
        n_sets_of_tickers = 11
        total_sleep_time = 0
        for sleep_for in range(n_sets_of_tickers):
            # sleep_for = random.uniform(0.05, 1.0)
            total_sleep_time += sleep_for
            queue.put_nowait({"n": sleep_for, "sleep_for": sleep_for})

        # Create three worker tasks to process the queue concurrently.
        tasks = []
        for i in range(n_sets_of_tickers):
            task = asyncio.create_task(self.workera(f'worker-{i}', queue))
            tasks.append(task)

        # Wait until the queue is fully processed.
        started_at = time.monotonic()
        await queue.join()
        total_slept_for = time.monotonic() - started_at

        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)
        await self.stream_options_dataa()

        # print('====')
        # print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
        # print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


    # ------  SP Option streaming handlers ---
    async def nasdaq_order_book_handler(self, msg):
        print("="*50)
        print("nasdaq_order_book_handler")
        print("-"*40)
        print(msg)
        print("="*50)

        for t_ in msg["content"]:
            bb = []
            aa = []
            for b in t_["BIDS"]:
                bb.append(b["BID_PRICE"])
            if len(bb) == 0:
                bb = 0
            else:
                bb = sum(bb)/len(bb)
            for a in t_["ASKS"]:
                aa.append(a["ASK_PRICE"])
            if len(aa) == 0:
                aa = 0
            else:
                aa = sum(aa)/len(aa)
            price = round(100*(bb+aa)/2)/100
            # print(price)

            if not t_["key"] in self.dic_share_prices:
                self.dic_share_prices["n__"] = 0
                self.dic_share_prices[t_["key"]] = {}

                d = datetime.datetime.fromtimestamp(t_["BOOK_TIME"] / 999.999451)
                h = d.hour
                m = d.minute
                date_ = d.date()
                time_ = str(date_) + ":" + str(h) + ":" + str(m)

                self.dic_share_prices[t_["key"]]["BOOK_TIME"] = time_
                self.dic_share_prices[t_["key"]]["LOW_PRICE"] = price
                self.dic_share_prices[t_["key"]]["HIGH_PRICE"] = price
                self.dic_share_prices[t_["key"]]["OPEN_PRICE"] = price
                self.dic_share_prices[t_["key"]]["CLOSE_PRICE"] = 0
            self.dic_share_prices[t_["key"]]["CLOSE_PRICE"] = price

            if price < self.dic_share_prices[t_["key"]]["LOW_PRICE"]:
                self.dic_share_prices[t_["key"]]["LOW_PRICE"] = price
            elif price > self.dic_share_prices[t_["key"]]["LOW_PRICE"]:
                self.dic_share_prices[t_["key"]]["HIGH_PRICE"] = price
        # print(self.dic_share_prices)
        n__ = self.dic_share_prices["n__"]
        n__ += 1
        self.dic_share_prices["n__"] = n__
        if n__ < 2:
            return
        n__ = self.dic_share_prices.pop("n__")

        print("="*30)
        print("processed nasdaq_order_book_handler")
        print("-"*20)
        print(self.dic_share_prices)
        print("="*50)

        return

        try:
            msg = json.dumps(self.dic_share_prices)
            print(json.dumps(self.dic_share_prices, indent=4))
            response_ = {
                'msg': msg,
                'type': "data_received_nasdaq_order_book"
            }
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'option1', {
                    'type': 'chat_message',
                    'text': json.dumps(response_)
                })
        except Exception as ex:
            pass
            # print(ex)
        self.dic_share_prices = {}

    async def option_order_book_handler(self, msg):
        print("="*50)
        print("option_order_book_handler")
        print("="*50)
        print(msg)

    async def level_one_option_handler(self, msg):
        print("="*50)
        print("level_one_option_handler")
        print("="*50)
        print(msg)

    async def timesale_options(self, msg):
        print("="*50)
        print("timesale_options_subs")
        print("="*50)
        print(msg)

    # for now this is the only function I use.
    async def chart_equity_handler(self, msg):
        # print("="*100)
        # print("chart_equity_handler")
        # await self.log_debug_async("1000 - chart_equity_handler")
        # print("-"*40)
        # print(msg)
        # print("="*100)
        dic = {}
        for t_ in msg["content"]:
            # d = datetime.datetime.fromtimestamp(t_["CHART_TIME"] / 999.999451)
            # h = d.hour
            # m = d.minute
            # # date_ = d.date()
            # time_ = str(d.day) + " " + calendar.month_abbr[d.month] + " " + str(d.year)+" "
            # time_ += self.add_zero(str(h)) + ":" + self.add_zero(str(m)) + " GMT"

            time_ = t_["CHART_TIME"]

            # '06 Nov 1994 20:49 GMT'
            o = t_["OPEN_PRICE"]
            h = t_["HIGH_PRICE"]
            l = t_["LOW_PRICE"]
            c = t_["CLOSE_PRICE"]
            v = round(t_["VOLUME"])
            dic[t_["key"]] = [time_, o, h, l, c, v]
        try:
            response_ = {
                'msg': dic,
                'type': "data_received_chart_equity"
            }

            # print(response_)

            await self.log_debug_async("1100 - chart_equity_handler - sending response")

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'option1', {
                    'type': 'chat_message',
                    'text': json.dumps(response_)
                })
            await self.record_data_received_chart_equity(dic)
        except Exception as ex:
            pass
            # print(ex)

    @database_sync_to_async
    def record_data_received_chart_equity(self, dic):
        for k in dic:
            ll = dic[k]
            try:
                r = XBRLRealEquityPrices.objects.create(ticker=k, t=ll[0], o=ll[1], h=ll[2], l=ll[3], c=ll[4], v=ll[5])
            except Exception as ex:
                pass

    def get_archived_data_from_db(self):
        msg_ = {}
        for q in XBRLRealEquityPrices.objects.all():
            try:
                if q.ticker not in msg_:
                    msg_[q.ticker] = []
                point_data = {'x': q.t, 'o': float(q.o), 'h': float(q.h), 'l': float(q.l), 'c': float(q.c)};
                msg_[q.ticker].append(point_data)
            except Exception as ex:
                log_debug("DataPointError: " + str() + str(ex))
        log_debug("get_archived_data_from_db 222")
        return msg_

    async def level_one_equity_handler(self, msg):
        print("="*50)
        print("level_one_equity_handler")
        print("-"*40)
        print(msg)
        print("="*50)

    # ---
    def activate_several_stream(self, dic):
        services = eval(dic)
        asyncio.run(self.read_several_stream(services))

    # -------------------------------------------------
    def place_order(self, dic):
        dic = json.loads(dic)
        print("="*100)
        print(dic)
        print("-"*10)
        print(dic["dic"]["q"])
        print("-"*50)

        order = {
            "orderStrategyType": "TRIGGER",
            "orderType": "LIMIT",
            "quantity": dic["dic"]["q"],
            "price": dic['limits']['sell_limit'],
            "duration": "DAY",
            "session": "NORMAL",
            "complexOrderStrategyType": "CUSTOM",
            "orderLegCollection": [],
            "childOrderStrategies": [
                {
                    "orderStrategyType": "SINGLE",
                    "orderType": "LIMIT",
                    "quantity": dic["dic"]["q"],
                    "price": dic['limits']['buy_limit'],
                    "duration": "GOOD_TILL_CANCEL",
                    "session": "NORMAL",
                    "complexOrderStrategyType": "CUSTOM",
                    "orderLegCollection": []
                }
            ]
        }
        # print(order)
        dic = dic["order"]
        for type_ in dic:
            if type_ in ["put", "call"]:
                for s_ in dic[type_]:
                    if dic[type_][s_]["q"] > 0:
                        order["orderLegCollection"].append(
                            {"instrument": {"assetType": "OPTION", "symbol": s_},
                             "instruction": "SELL_TO_OPEN", "quantity": dic[type_][s_]["q"]})
                        order["childOrderStrategies"][0]["orderLegCollection"].append(
                            {"instrument": {"assetType": "OPTION", "symbol": s_},
                             "instruction": "BUY_TO_CLOSE", "quantity": dic[type_][s_]["q"]})
                    else:
                        order["orderLegCollection"].append(
                            {"instrument": {"assetType": "OPTION", "symbol": s_},
                             "instruction": "BUY_TO_OPEN", "quantity": -dic[type_][s_]["q"]})
                        order["childOrderStrategies"][0]["orderLegCollection"].append(
                            {"instrument": {"assetType": "OPTION", "symbol": s_},
                             "instruction": "SELL_TO_CLOSE", "quantity": -dic[type_][s_]["q"]})

        print("-1"*50)
        print(order)
        print("-1"*50)
        return {'data': order}

    def place_order_test(self, dic):
        dic = json.loads(dic)
        print("="*100)
        print(dic)
        print("-"*50)

        # from tda.orders.equities import equity_buy_limit
        eq = orders.equities.equity_buy_limit(dic["ticker"], 2, 1250.0).set_duration(Duration.GOOD_TILL_CANCEL).set_session(Session.SEAMLESS).build()
        print(eq)
        print(type(eq))
        print("-"*50)
        o = orders.options.option_buy_to_open_limit("TSLA_022522C985", 1, 5).build()
        print(o)
        print("-"*50)
        ca = orders.options.bear_call_vertical_open("TSLA_022522C985", "TSLA_022522C990", 5, 1.3)
        ca.set_duration(Duration.GOOD_TILL_CANCEL)
        ca.set_quantity(10)
        print(ca.build())
        print("-"*50)
        # c = self.get_stream_client()
        # c.place_order(self.account_id, ca.build())
        return {'data': order}

    def place_order_(self, dic):
        print(dic)
        print("="*50)
        # a = orders.options.option_buy_to_open_market("TSLA_021122P840", 1)
        ca = orders.options.bear_call_vertical_open("TSLA_021122C985", "TSLA_021122C990", 100, 1.3)
        ca.set_duration(Duration.GOOD_TILL_CANCEL)
        # ac.set_quantity(10)
        print(ca.build())
        print("-"*30)
        cb = orders.options.bear_call_vertical_close("TSLA_021122C985", "TSLA_021122C990", 100, 0.8)
        cb.set_duration(Duration.GOOD_TILL_CANCEL)
        print(cb.build())

        print("="*40)
        pa = orders.options.bull_put_vertical_open("TSLA_021122P845", "TSLA_021122P850", 10, 1.1)
        pa.set_duration(Duration.GOOD_TILL_CANCEL)
        print(pa.build())
        print("-"*30)
        pb = orders.options.bull_put_vertical_close("TSLA_021122P845", "TSLA_021122P850", 10, 0.95)
        pb.set_duration(Duration.GOOD_TILL_CANCEL)
        print(pb.build())
        # self.client.place_order(self.account_id, order_spec=a.build())

        print("="*100)
        cab = orders.common.first_triggers_second(ca, cb)
        print(cab.build())
        print("="*100)
        pab = orders.common.first_triggers_second(pa, pb)
        print(pab.build())
        print("="*100)

        return {'status': 'ok'}

    # def place_order_test(self, dic):
    #     dic = json.loads(dic)
    #     print("="*100)
    #     print(dic)
    #     print("-"*50)
    #
    #     o = orders.options.option_buy_to_open_limit("TSLA_022522C985", 1, 5).build()
    #     print(o)
    #     print("-"*50)
    #     ca = orders.options.bear_call_vertical_open("TSLA_022522C985", "TSLA_022522C990", 5, 1.3)
    #     ca.set_duration(Duration.GOOD_TILL_CANCEL)
    #     ca.set_quantity(10)
    #     print(ca.build())
    #     print("-"*50)
    #
    #     # c = self.get_stream_client()
    #     # c.place_order(self.account_id, ca.build())
    #
    #     return {'data': order}

    def account_test(self, dic):
        dic = json.loads(dic)
        result = {}
        try:
            c = self.get_client()
            so_ = {
                "orderType": "NET_CREDIT",
                "session": "NORMAL",
                "quantity": 1,
                "price": "1.20",
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "BUY_TO_OPEN",
                        "quantity": 1,
                        "instrument": {
                            "symbol": "TSLA_022522C990",
                            "assetType": "OPTION"
                        }
                    },
                    {
                        "instruction": "SELL_TO_OPEN",
                        "quantity": 1,
                        "instrument": {
                            "symbol": "TSLA_022522C985",
                            "assetType": "OPTION"
                        }
                    }
                ]
            }
            try:
                so = c.create_saved_order(self.account_id, so_)
            except Exception as ex:
                print(ex)
            try:
                co = c.get_saved_orders_by_path(self.account_id)
            except Exception as ex:
                print(ex)
        except Exception as ex:
            print(ex)

        return {'data': result}

    def create_option_symbol(self, ticker):
        symbol = ticker
        return symbol


class AcademyCityXBRL(object):
    def __init__(self):

        # Should remove it later on
        try:
            clear_log_debug()
        except Exception as ex:
            pass
        #
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

        self.TEXT_PATH = os.path.join(self.TO_DATA_PATH, "text")
        os.makedirs(self.TEXT_PATH, exist_ok=True)
        # print(self.TEXT_PATH)

        self.XBRL_PATH = os.path.join(self.TO_DATA_PATH, "xbrl")
        os.makedirs(self.XBRL_PATH, exist_ok=True)
        # print(self.XBRL_PATH)

        self.Data = None
        self.sp_tickers = []
        self.xbrl_base_year = 2020
        self.xbrl_start_year = 2012
        self.today_year = datetime.datetime.now().year
        # log_debug("AcademyCityXBRL was created")`
        self.matching_accounts = None

    # Valuation Functions
    def get_risk_premium(self, year10=1928, year50=1928, cv_project_id=None, is_update='no'):
        log_debug("Start get_risk_premium.")
        base_year = 1928
        project = Project.objects.filter(translations__language_code=get_language()).get(id=int(cv_project_id))
        # print(is_update)
        if is_update != 'yes':
            if project.dic_data:
                return project.dic_data
        dic = {'Arithmetic': {}, 'Geometric': {}}
        try:
            # l_years = [base_year, year50, year10]
            l_years = range(base_year, datetime.datetime.now().year)
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

                log_debug('Start process year : ' + str(y))
                ll = [[rp.return_on_sp500, rp.tb3ms_rate, rp.return_on_tbond] for rp in
                      XBRLHistoricalReturnsSP.objects.filter(year__gte=y).all()]
                df = pd.DataFrame(ll)
                df.columns = ['M', 'TB', 'B']
                df['M_TB'] = df['M'] - df['TB']
                df['M_B'] = df['M'] - df['B']

                llb = [[rp.return_on_sp500, rp.tb3ms_rate, rp.return_on_tbond] for rp in
                       XBRLHistoricalReturnsSP.objects.filter(year__lte=y).filter(year__gte=base_year).all()]
                dfb = pd.DataFrame(llb)
                dfb.columns = ['M', 'TB', 'B']
                dfb['M_TB'] = dfb['M'] - dfb['TB']
                dfb['M_B'] = dfb['M'] - dfb['B']
                log_debug('process year : ' + str(y) + " ll done")

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

                dic['Arithmetic'][y]['Stocks-TBills']['value'] = round(10000 * df.mean()['M_TB']) / 10000
                dic['Arithmetic'][y]['Stocks-TBonds']['value'] = round(10000 * df.mean()['M_B']) / 10000

                yrp = XBRLHistoricalReturnsSP.objects.get(year=y)

                log_debug('process year : ' + str(y) + " yrp done")

                dic['Arithmetic'][y]['Stocks-TBonds']['sp500'] = yrp.return_on_sp500
                dic['Arithmetic'][y]['Stocks-TBonds']['tb3ms'] = yrp.tb3ms_rate
                dic['Arithmetic'][y]['Stocks-TBonds']['tbond'] = yrp.return_on_tbond
                dic['Arithmetic'][y]['Stocks-TBonds']['m_b_median'] = round(10000 * df.median()['M_B']) / 10000
                #
                dic['Arithmetic'][y]['Stocks-TBonds']['b_value'] = round(10000 * dfb.mean()['M_B']) / 10000
                dic['Arithmetic'][y]['Stocks-TBonds']['b_m_b_median'] = round(10000 * dfb.median()['M_B']) / 10000
                #
                log_debug('process year : ' + str(y) + " calculation 1 done")

                try:
                    dic['Arithmetic'][y]['Stocks-TBills']['std'] = round(
                        10000 * df.std()['M_TB'] / ((df.shape[0] + 1) ** (1 / 2))) / 10000
                    dic['Arithmetic'][y]['Stocks-TBonds']['std'] = round(
                        10000 * df.std()['M_B'] / ((df.shape[0] + 1) ** (1 / 2))) / 10000

                    dic['Arithmetic'][y]['Stocks-TBonds']['b_std'] = round(
                        10000 * dfb.std()['M_B'] / ((dfb.shape[0] + 1) ** (1 / 2))) / 10000
                    log_debug('process year : ' + str(y) + " std calculation 2 done")
                except Exception as exx:
                    log_debug('Error 10 : ' + " " + str(y) + " " + str(exx))
                gm = 1
                gtb = 1
                gb = 1
                for i, r in df.iterrows():
                    gm *= (1 + r['M'])
                    gtb *= (1 + r['TB'])
                    gb *= (1 + r['B'])
                gm = gm ** (1 / df.shape[0]) - 1
                gtb = gtb ** (1 / df.shape[0]) - 1
                gb = gb ** (1 / df.shape[0]) - 1

                dic['Geometric'][y]['Stocks-TBills']['value'] = round(10000 * (gm - gtb)) / 10000
                dic['Geometric'][y]['Stocks-TBonds']['value'] = round(10000 * (gm - gb)) / 10000
                dic['Geometric'][y]['Stocks-TBills']['std'] = ''
                dic['Geometric'][y]['Stocks-TBonds']['std'] = ''

                try:
                    bgm = 1
                    bgtb = 1
                    bgb = 1
                    for i, r in dfb.iterrows():
                        bgm *= (1 + r['M'])
                        # bgtb *= (1+r['TB'])
                        bgb *= (1 + r['B'])
                    bgm = bgm ** (1 / dfb.shape[0]) - 1
                    # bgtb = bgtb**(1/dfb.shape[0]) - 1
                    bgb = bgb ** (1 / dfb.shape[0]) - 1
                    dic['Geometric'][y]['Stocks-TBonds']['b_value'] = round(10000 * (bgm - bgb)) / 10000
                except Exception as ex:
                    print('ex')
                    print(ex)
                    print('ex')

                log_debug('End process year : ' + str(y))

            # Damodarad uses geometric:  dic['Geometric'][1928]['Stocks-TBonds']['value']
            project.mature_marker_risk_premium = dic['Arithmetic'][1928]['Stocks-TBonds']['value']
            project.dic_data = dic
            project.save()
            # print(dic)

        except Exception as ex:
            log_debug('Error 10 : ' + " " + str(ex))

        log_debug("End get_risk_premium.")
        return dic

    # Assisting functions
    def download_excel_file(self, url, file, ext='xlsx'):
        path = os.path.join(self.EXCEL_PATH, file + "." + ext)
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
    def get_statements(self, company):
        statements = {}
        for statement in XBRLValuationStatementsAccounts.objects.all():
            statements[statement.order] = {'name': statement.statement, 'accounts': {}}
            sic_ = company.industry.sic_code
            sic__ = company.industry.main_sic.sic_code
            accounts = statement.xbrl_valuation_statements.filter(Q(sic=0) | Q(sic=sic_) | Q(sic=sic__)).all()

            for a in accounts:
                statements[statement.order]['accounts'][a.order] = [a.account, a.type, a.scale]
        # print(statements)
        return statements

    # --
    async def process_page(self, obj, text, url, dic):
        print("process_page")
        print(obj.name)
        # print(text)
        print(url)
        print(dic)
        n = np.random.randn()
        dic['url'+str(n)] = url
        asyncio.sleep(1)
        return {"k1": "amob"}

    def run_all_pages(self, dic):
        print('='*50)
        dic = eval(dic)
        print(dic)
        print('='*50)

        urls = ['https://www.sec.gov/Archives/edgar/data/320193/000119312512444068/aapl-20120929.xml',
                'https://www.sec.gov/Archives/edgar/data/320193/000119312513416534/aapl-20130928.xml']

        gaup = GetAllUrlsProcessed()
        k = asyncio.run(gaup.process_all_pages(urls, func=self.process_page, dic=dic))
        print('='*50)
        print(dic)
        print('='*50)
        print('k')
        print(k)

    # --
    def get_data_ticker(self, ticker, is_update='no', is_updateq='no'):
        try:
            company = XBRLCompanyInfo.objects.get(ticker=ticker)
        except Exception as ex:
            print("Error 666" + str(ex))
        dataq = ""
        if is_update == "no" and company.financial_data:
            dic_company_info = company.financial_data
            # print(dic_company_info)
            if is_updateq == "no" and company.financial_dataq:
                # print('dic_company_info q 2')
                dataq = company.financial_dataq
            elif is_updateq == "yes":
                dataq = self.get_dic_company_info_q_(company, dic_company_info)
                company.financial_dataq = dataq
                company.save()
        else:
            dic_company_info = self.get_dic_company_info(company)
            # print('-2'*50)
            company.financial_data = dic_company_info
            # print('-3'*50)
            company.save()
        try:
            countries_regions_ = company.get_countries_regions()
            dic_company_info["countries_regions"] = countries_regions_
        except Exception as ex:
            log_debug("get_dic_company_info ex1: " + str(ex))
        result = {'dic_company_info': dic_company_info, 'dataq': dataq}
        # print(result)
        return result

    def get_dic_company_info(self, company, type_="10-K"):
        dic_company_info = self.get_dic_company_info_(company, type_)
        # print(dic_company_info)
        dic_data = dic_company_info['data']
        if len(dic_data) == 0:
            try:
                dic_company_info = self.get_dic_company_info_(company, "20-F")
                dic_data = dic_company_info['data']
            except Exception as ex:
                pass
            if len(dic_data) == 0:
                return dic_company_info
        if 'statements' not in dic_company_info:
            dic_company_info['statements'] = self.get_statements(company=company)
        dic_company_info = self.process_dic_company_info_(dic_company_info)
        # print(dic_company_info)
        return dic_company_info

    def get_dic_company_info_(self, company, type_="10-K"):
        clear_log_debug()
        # print("get_dic_company_info_ 1")
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&count=100"  # &dateb={}"
        url = base_url.format(company.cik, type_)
        # print('-1'*10)
        # print(url)
        dic_company_info = {"company_info": {'ticker': company.ticker,
                                             'cik': company.cik,
                                             'sic_code': company.industry.sic_code,
                                             'marginal_tax_rate': str(company.tax_rate),
                                             '10k_url': url,
                                             },
                            'data': {}}
        # print(dic_company_info)
        headers = {'User-Agent': 'amos@drbaranes.com'}
        edgar_resp = requests.get(url, headers=headers, timeout=30)
        # print("Current Time 11 =", datetime.datetime.now().strftime("%H:%M:%S"))
        edgar_str = edgar_resp.text
        # print(edgar_str)
        #
        cik0 = ''
        cik_re = re.compile(r'.*CIK=(\d{10}).*')
        results = cik_re.findall(edgar_str)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            cik0 = str(results[0])
        dic_company_info['company_info']['cik'] = cik0
        #
        sic0 = ''
        cik_re = re.compile(r'.*SIC=(\d{4}).*')
        results = cik_re.findall(edgar_str)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            sic0 = str(results[0])
        dic_company_info['company_info']['SIC'] = sic0
        # print('-3'*10)
        # print(dic_company_info)
        # print('-3'*10)
        #
        # Find the document links
        soup = BeautifulSoup(edgar_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile2')
        try:
            rows = table_tag.find_all('tr')
        except Exception as ex:
            return dic_company_info

        # Obtain HTML for document page
        dic_data = {}
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) > 3:
                    if cells[0].text.lower() != type_.lower():
                        continue
                    # for filing_year in range(2019, 2020):
                    for filing_year in range(self.xbrl_start_year, self.today_year + 1):
                        if str(filing_year) in cells[3].text:
                            # print(str(filing_year), cells[3].text, cells[1].a['href'], cells[0].text)
                            if filing_year not in dic_data and (cells[0].text == "10-K" or cells[0].text == "20-F"):
                                dic_data[filing_year] = {}
                                dic_data[filing_year]['href'] = 'https://www.sec.gov' + cells[1].a['href']
            except Exception as ex:
                pass

        dic_company_info['data'] = dic_data
        # print(dic_company_info)
        return dic_company_info

    def process_dic_company_info_(self, dic_company_info):
        urls = []
        max_y = 0
        for y in dic_company_info['data']:
            # print(dic_company_info['data'][y])
            urls.append(dic_company_info['data'][y]["href"])
            if max_y < y:
                max_y = y
        max_y += 1
        dic_matching_accounts = self.get_matching_accounts_(dic_company_info, max_y)
        dic_ = {"dic_company_info": dic_company_info, "dic_matching_accounts": dic_matching_accounts}
        # --
        gaup = GetAllUrlsProcessed()
        k = asyncio.run(gaup.process_all_pages(urls, func=self.get_data_for_years_async, dic=dic_))
        # --
        dic_company_info = dic_["dic_company_info"]
        return dic_company_info

    async def get_data_for_years_async(self, obj, txt, url, dic):
        dic_company_info = dic["dic_company_info"]
        dic_matching_accounts = dic["dic_matching_accounts"]
        try:
            value = None
            key = None
            for y in dic_company_info["data"]:
                if dic_company_info["data"][y]["href"] == url:
                    value = dic_company_info["data"][y]
                    key = y
            doc_str = txt
            xbrl_link = ''
            soup = BeautifulSoup(doc_str, 'html.parser')
            table_tag = soup.find('table', class_='tableFile', summary='Data Files')
        except Exception as ex:
            print("Error 22: " + str(ex))
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
            value['xbrl_link'] = 'https://www.sec.gov' + xbrl_link
            accession_number = xbrl_link.split('/')
            view_link = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='
            view_link += accession_number[4] + '&accession_number=' + accession_number[5] + '&xbrl_type=v#'

            r_link = "https://www.sec.gov/Archives/edgar/data/" + accession_number[4] + "/" + accession_number[5] + "/R"
            value['r_link'] = r_link
            value['view_link'] = view_link
        except Exception as ex:
            # print("Error 67: " + str(ex))
            return value

        xbrl_str = await obj.get_page(value['xbrl_link'])
        soup = BeautifulSoup(xbrl_str, 'lxml')
        value['dei'] = {}
        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            value['dei'][name_[1]] = tag.text

        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(value)
        # print(key)
        # # print(txt)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)
        # print(str(key) + '-11'*20)

        documentperiodenddate = value['dei']['documentperiodenddate']
        entitycentralindexkey = value['dei']['entitycentralindexkey']
        y_ = int(value['dei']['documentfiscalyearfocus'])
        # For ticker ANTM there is a problem for year 2014 it shows documentfiscalyearfocus=2013 when it should be 2014
        # I left that error, so I miss data for 2014
        # y_ = int(str(documentperiodenddate).split("-")[0])
        try:
            s_cik = "NA"
            flow_context_id = ""
            for tag in soup.find_all(name=re.compile('enddate'), string=documentperiodenddate):
                # print(tag.name)
                try:
                    context = tag.find_parent(re.compile('context'))
                    context_name = context.name.split(":")
                    if len(context_name) > 1:
                        identifier = context.find(context_name[0] + ':identifier')
                        segment = context.find(context_name[0] + ':segment')
                        startdate = context.find(context_name[0] + ':startdate')
                    else:
                        identifier = context.find('identifier')
                        segment = context.find('segment')
                        startdate = context.find('startdate')

                    end_date = tag.text.split('-')
                    start_date = startdate.text.split('-')
                    start_date = start_date[0] + '-' + start_date[1]

                    start_date_should = str((int(end_date[0]) - 1)) + '-' + end_date[1]
                    start_date0_should = str((int(end_date[0]) - 2)) + '-12'
                    if int(end_date[1]) > 10 or int(end_date[1]) < 3:
                        start_date1_should = end_date[0] + '-01'
                    else:
                        start_date1_should = 0
                    start_date2_should = str((int(end_date[0]) - 1)) + '-' + self.add_zero(str((int(end_date[1]) + 1)))
                    start_date3_should = str((int(end_date[0]) - 1)) + '-' + self.add_zero(str((int(end_date[1]) - 1)))

                    if (not segment) and (identifier.text == entitycentralindexkey) \
                            and (
                            start_date == start_date_should or start_date == start_date0_should or
                            start_date == start_date1_should or start_date == start_date2_should or
                            start_date == start_date3_should):
                        # if int(y_) == 2014:
                        #     print("-=3"*3)
                        #     print(end_date, context['id'], start_date_should, start_date0_should, start_date1_should,start_date2_should,start_date3_should)
                        #     print(context)
                        flow_context_id = context['id']
                    if flow_context_id == "":
                        s_cik = dic_company_info['company_info']['cik']
                        while len(s_cik) < 10:
                            s_cik = "0" + s_cik
                        if (not segment) and (identifier.text == s_cik) and (
                                start_date == start_date_should or start_date == start_date0_should or
                                start_date == start_date1_should or start_date == start_date2_should or
                                start_date == start_date3_should
                        ):
                            flow_context_id = context['id']
                    else:
                        break

                except Exception as ex:
                    # print(ex)
                    continue

            instant_context_id = ""
            for tag in soup.find_all(name=re.compile('instant'), string=documentperiodenddate):
                context = tag.find_parent(re.compile('context'))

                context_name = context.name.split(":")

                if len(context_name) > 1:
                    identifier = context.find(context_name[0] + ':identifier')
                    segment = context.find(context_name[0] + ':segment')
                else:
                    identifier = context.find('identifier')
                    segment = context.find('segment')
                if not segment and identifier.text == entitycentralindexkey:
                    # print(context)
                    instant_context_id = context['id']

                if instant_context_id == "":
                    s_cik = dic_company_info['company_info']['cik']
                    while len(s_cik) < 10:
                        s_cik = "0" + s_cik
                    if not segment and identifier.text == s_cik:
                        # print(context)
                        instant_context_id = context['id']
        except Exception as ex:
            return value
        try:
            matching_accounts = dic_matching_accounts[y_]["matching_accounts"]
            accounts_ = dic_matching_accounts[y_]["accounts_"]
            used_accounting_standards = dic_matching_accounts[y_]["used_accounting_standards"]

            value['matching_accounts'] = matching_accounts
            year_data = {}

            accounts_flow = {}
            for k in accounts_['flow']:
                accounts_flow[k[0:92]] = accounts_['flow'][k]

            accounts_instant = {}
            for k in accounts_['instant']:
                accounts_instant[k[0:92]] = accounts_['instant'][k]

            for std in used_accounting_standards:
                tag_list = soup.find_all(re.compile(std + ":"))
                for tag in tag_list:
                    name_ = tag.name.split(":")
                    try:
                        if instant_context_id != "":
                            if name_[1][0:92] in accounts_instant and tag['contextref'] == instant_context_id:
                                if accounts_instant[name_[1][0:92]][2] == std:
                                    order = accounts_instant[name_[1][0:92]][0]
                                    scale = accounts_instant[name_[1][0:92]][1]
                                    if scale == 1:
                                        year_data[order] = tag.text
                                    else:
                                        year_data[order] = int(round(float(tag.text))) / scale
                        if name_[1][0:92] in accounts_flow:
                            if tag['contextref'] == flow_context_id and accounts_flow[name_[1][0:92]][2] == std:
                                order = accounts_flow[name_[1][0:92]][0]
                                scale = accounts_flow[name_[1][0:92]][1]
                                if scale == 1:
                                    year_data[order] = tag.text
                                else:
                                    year_data[order] = int(round(float(tag.text))) / scale
                    except Exception as ex:
                        pass
                        # print("Error: " + str(ex))
            value['year_data'] = year_data
            dic_company_info['data'][key] = value
        except Exception as ex:
            return value
        return value

    def get_matching_accounts_(self, dic_company_info, max_y):
        ticker = dic_company_info['company_info']['ticker']
        sic = dic_company_info['company_info']['SIC']
        statements = dic_company_info['statements']
        dic = {}
        for year in range(2011, max_y):
            dic[year] = {}
            try:
                if year <= self.xbrl_base_year:
                    years = sorted(range(year, self.xbrl_base_year + 1), reverse=True)
                else:
                    years = range(self.xbrl_base_year, year + 1)
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

            matching_accounts = {}
            accounts_ = {'instant': {}, 'flow': {}}

            for st_ in statements:
                for a_order in statements[st_]['accounts']:
                    try:
                        if int(a_order) in dic_matches:
                            ma_, ma_std = dic_matches[int(a_order)][0].lower(), dic_matches[int(a_order)][1].lower()
                        else:
                            ma_, ma_std = "", ""
                    except Exception as ex:
                        pass

                    if ma_ != '':
                        if statements[st_]['accounts'][a_order][1] == 1:
                            accounts_['instant'][ma_] = (a_order, statements[st_]['accounts'][a_order][2], ma_std)
                        else:
                            accounts_['flow'][ma_] = (a_order, statements[st_]['accounts'][a_order][2], ma_std)
                    matching_accounts[a_order] = [ma_, ma_std]
            dic[year]["matching_accounts"] = matching_accounts
            dic[year]["accounts_"] = accounts_
            dic[year]["used_accounting_standards"] = used_accounting_standards
        return dic

    #  --
    def get_dic_company_info_q_(self, company, dic_company_info):

        headers = {'User-Agent': 'amos@drbaranes.com'}
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&count=100"  # &dateb={}"
        type_ = '10-Q'
        url_q = base_url.format(company.cik, type_)
        dic_data = {'10q_url': url_q, 'data': {}}
        try:
            edgar_resp_q = requests.get(url_q, headers=headers, timeout=30)
        except Exception as ex:
            print(str(ex))
        edgar_str_q = edgar_resp_q.text
        soup_q = BeautifulSoup(edgar_str_q, 'html.parser')
        table_tag_q = soup_q.find('table', class_='tableFile2')
        try:
            rows = table_tag_q.find_all('tr')
        except Exception as ex:
            return dic_company_info
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) > 3:
                    if cells[0].text.lower() != type_.lower():
                        continue
                    for filing_year in range(self.xbrl_start_year, self.today_year + 1):
                        if str(filing_year) in cells[3].text:
                            m = cells[3].text.split("-")[1]
                            try:
                                if filing_year not in dic_data['data']:
                                    dic_data['data'][filing_year] = {}
                            except Exception as exx:
                                print(str(exx))
                            dic_data['data'][filing_year][m] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
            except Exception as ex:
                pass
        urls = []
        max_y = 0
        for key in dic_data['data']:
            if max_y<key:
                max_y=key
            try:
                url_ = dic_company_info['data'][str(key)]['href']
                dic_data['data'][key]['Q4'] = {'href': url_}
            except Exception as ex:
                dic_data['data'][key]['Q4'] = {'href': ""}
            for m in dic_data['data'][key]:
                if dic_data['data'][key][m]['href'] == "":
                    continue
                else:
                    urls.append(dic_data['data'][key][m]['href'])
        max_y += 1
        dic_matching_accounts = self.get_matching_accounts_(dic_company_info, max_y)
        s_cik = str(company.cik)
        while len(s_cik) < 10:
            s_cik = "0" + s_cik
        dic_ = {"dic_data": dic_data, "dic_matching_accounts": dic_matching_accounts, "cik": s_cik}
        # --
        gaup = GetAllUrlsProcessed()
        k = asyncio.run(gaup.process_all_pages(urls, func=self.get_data_for_one_year_q_async, dic=dic_))
        return dic_["dic_data"]

    async def get_data_for_one_year_q_async(self, obj, txt, url, dic):
        dic_data = dic["dic_data"]
        s_cik = dic["cik"]
        # print(s_cik)
        dic_matching_accounts = dic["dic_matching_accounts"]
        value = None
        key = None
        m = None
        for y in dic_data["data"]:
            for m_ in dic_data["data"][y]:
                try:
                    if dic_data["data"][y][m_]["href"] == url:
                        value = dic_data["data"][y][m_]
                        key = y
                        m = m_
                except Exception as ex:
                    continue
        xbrl_link = ''
        soup = BeautifulSoup(txt, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')
        # print(table_tag)
        try:
            rows = table_tag.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 3:
                    if 'INS' in cells[3].text or 'XML' in cells[3].text:
                        # print(cells[3].text)
                        xbrl_link = cells[2].a['href']
            value['xbrl_link'] = 'https://www.sec.gov' + xbrl_link
            accession_number = xbrl_link.split('/')
            view_link = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='
            view_link += accession_number[4] + '&accession_number=' + accession_number[5] + '&xbrl_type=v#'

            r_link = "https://www.sec.gov/Archives/edgar/data/" + accession_number[4] + "/" + accession_number[5] + "/R"
            value['r_link'] = r_link
            value['view_link'] = view_link
        except Exception as ex:
            return value

        # xbrl_resp = requests.get(value['xbrl_link'], headers=headers, timeout=30)
        # xbrl_str = xbrl_resp.text
        # print(value['xbrl_link'])
        xbrl_str = await obj.get_page(value['xbrl_link'])

        soup = BeautifulSoup(xbrl_str, 'lxml')
        value['dei'] = {}
        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            value['dei'][name_[1]] = tag.text

        documentperiodenddate = value['dei']['documentperiodenddate']
        entitycentralindexkey = value['dei']['entitycentralindexkey']
        if m == "Q4":
            documentfiscalperiodfocus = "Q4"
            value['dei']['documentfiscalperiodfocus'] = "Q4"
        else:
            documentfiscalperiodfocus = value['dei']['documentfiscalperiodfocus']

        flow_context_id = ""
        for tag in soup.find_all(name=re.compile('enddate'), string=documentperiodenddate):
            try:
                context = tag.find_parent(re.compile('context'))
                # print(context)
                context_name = context.name.split(":")

                if len(context_name) > 1:
                    identifier = context.find(context_name[0] + ':identifier')
                    segment = context.find(context_name[0] + ':segment')
                    startdate = context.find(context_name[0] + ':startdate')
                else:
                    identifier = context.find('identifier')
                    segment = context.find('segment')
                    startdate = context.find('startdate')

                end_date = tag.text.split('-')
                start_date = startdate.text.split('-')
                start_date = start_date[0] + '-' + start_date[1]

                if 12 >= int(end_date[1]) > 4:
                    start_date_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 3))
                    start_date0_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 2))
                    start_date1_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 4))
                    start_date2_should = "none"
                    # print(start_date_should)
                elif int(end_date[1]) <= 4:
                    start_date_should = end_date[0] + '-01'
                    start_date0_should = end_date[0] + '-02'
                    start_date1_should = str((int(end_date[0]) - 1)) + '-12'
                    start_date2_should = str((int(end_date[0]) - 1)) + '-11'

                if (not segment) and (identifier.text == entitycentralindexkey) \
                        and (start_date == start_date_should or start_date == start_date0_should or
                             start_date == start_date1_should or start_date == start_date2_should):
                    flow_context_id = context['id']
                if flow_context_id == "":
                    if (not segment) and (identifier.text == s_cik) \
                            and (start_date == start_date_should or start_date == start_date0_should or
                                 start_date == start_date1_should or start_date == start_date2_should):
                        flow_context_id = context['id']

            except Exception as ex:
                # print(ex)
                continue

        # print('flow_context_id')
        # print(flow_context_id)
        # print('entitycentralindexkey')
        # print(entitycentralindexkey)
        # print('s_cik')
        # print(s_cik)

        instant_context_id = ""
        for tag in soup.find_all(name=re.compile('instant'), string=documentperiodenddate):
            context = tag.find_parent(re.compile('context'))
            context_name = context.name.split(":")
            if len(context_name) > 1:
                identifier = context.find(context_name[0] + ':identifier')
                segment = context.find(context_name[0] + ':segment')
            else:
                identifier = context.find('identifier')
                segment = context.find('segment')
            if not segment and identifier.text == entitycentralindexkey:
                # print(context)
                instant_context_id = context['id']
                if instant_context_id == "":
                    if not segment and identifier.text == s_cik:
                        instant_context_id = context['id']
        # print(instant_context_id)

        matching_accounts = dic_matching_accounts[key]["matching_accounts"]
        accounts_ = dic_matching_accounts[key]["accounts_"]
        used_accounting_standards = dic_matching_accounts[key]["used_accounting_standards"]

        value['matching_accounts'] = matching_accounts
        year_data = {}
        accounts_flow = {}
        for k in accounts_['flow']:
            accounts_flow[k[0:92]] = accounts_['flow'][k]

        accounts_instant = {}
        for k in accounts_['instant']:
            accounts_instant[k[0:92]] = accounts_['instant'][k]

        for std in used_accounting_standards:
            tag_list = soup.find_all(re.compile(std + ":"))
            for tag in tag_list:
                name_ = tag.name.split(":")
                try:
                    if name_[1][0:92] in accounts_instant and tag['contextref'] == instant_context_id:
                        if accounts_instant[name_[1][0:92]][2] == std:
                            order = accounts_instant[name_[1][0:92]][0]
                            scale = accounts_instant[name_[1][0:92]][1]
                            if scale == 1:
                                year_data[order] = tag.text
                            else:
                                year_data[order] = int(round(float(tag.text))) / scale
                    if name_[1][0:92] in accounts_flow and tag['contextref'] == flow_context_id:
                        if accounts_flow[name_[1][0:92]][2] == std:
                            order = accounts_flow[name_[1][0:92]][0]
                            scale = accounts_flow[name_[1][0:92]][1]
                            if scale == 1:
                                year_data[order] = tag.text
                            else:
                                year_data[order] = int(round(float(tag.text))) / scale
                except Exception as ex:
                    pass
                    # print("Error: year=" + str(dic_data_year[0]) + "   dic=" + dic_data_year[1]['href'] + "   " + str(ex) + tag.text)

        value['year_data'] = year_data
        dic_data['data'][key][m] = value
        return value

    # --
    # to be deleted
    def get_data_for_one_year(self, key, dic_company_info):
        value = dic_company_info['data'][key]
        temp = [key, value,
                dic_company_info['company_info']['SIC'], dic_company_info['company_info']['ticker'],
                dic_company_info['statements']
                ]
        dic_company_info['data'][key] = self.get_data_for_years(dic_data_year=temp)[1]
        return dic_company_info

    # to be deleted
    def get_data_for_years(self, dic_data_year):
        # print(dic_data_year)
        log_debug("start get_data_for_years: " + dic_data_year[3] + ", " + str(dic_data_year[0]))
        # print("Current Time Start get data = " + str(dic_data_year[0]), datetime.datetime.now().strftime("%H:%M:%S"))
        # dic_data_year[3] = ticker
        # dic_data_year[0] = year
        # dic_data_year[2] = sic
        #
        # print('-30'*10)
        # print(str(dic_data_year[0]) + dic_data_year[1]['href'])
        # print('-30'*10)

        headers = {'User-Agent': 'amos@drbaranes.com'}
        # print(dic_data_year[1])

        doc_resp = requests.get(dic_data_year[1]['href'], headers=headers, timeout=30)
        doc_str = doc_resp.text

        # print("get_data_for_years (after getting file_name): "+dic_data_year[3]+", "+str(dic_data_year[0]))

        # Find the XBRL link
        xbrl_link = ''
        soup = BeautifulSoup(doc_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')

        # print(dic_data_year[0])
        # print(dic_data_year[1]['href'])

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
            # print('-12-'*10)
            # print(accession_number)
            # print('-12-'*10)

            view_link = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='
            view_link += accession_number[4] + '&accession_number=' + accession_number[5] + '&xbrl_type=v#'

            r_link = "https://www.sec.gov/Archives/edgar/data/" + accession_number[4] + "/" + accession_number[5] + "/R"
            dic_data_year[1]['r_link'] = r_link
            dic_data_year[1]['view_link'] = view_link

        except Exception as ex:
            return dic_data_year

        xbrl_file_name = "xbrl_" + dic_data_year[3] + "_" + str(dic_data_year[0])
        # try:
        #     xbrl_str = request.session[xbrl_file_name]
        # except Exception as exc:
        xbrl_resp = requests.get(dic_data_year[1]['xbrl_link'], headers=headers, timeout=30)
        xbrl_str = xbrl_resp.text
        # request.session[xbrl_file_name] = xbrl_str

        # log_debug("get_data_for_years (after getting xbrl_file_name): "+dic_data_year[3]+", "+str(dic_data_year[0]))
        soup = BeautifulSoup(xbrl_str, 'lxml')
        dic_data_year[1]['dei'] = {}
        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            dic_data_year[1]['dei'][name_[1]] = tag.text

        documentperiodenddate = dic_data_year[1]['dei']['documentperiodenddate']
        entitycentralindexkey = dic_data_year[1]['dei']['entitycentralindexkey']

        # print(documentperiodenddate)
        # print(entitycentralindexkey)

        # print("Current Time 4 =", datetime.datetime.now().strftime("%H:%M:%S"))
        flow_context_id = ""
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
                    segment = context.find(context_name[0] + ':segment')
                    startdate = context.find(context_name[0] + ':startdate')
                else:
                    identifier = context.find('identifier')
                    segment = context.find('segment')
                    startdate = context.find('startdate')

                end_date = tag.text.split('-')
                start_date = startdate.text.split('-')
                start_date = start_date[0] + '-' + start_date[1]

                start_date_should = str((int(end_date[0]) - 1)) + '-' + end_date[1]
                start_date0_should = str((int(end_date[0]) - 2)) + '-12'
                if int(end_date[1]) > 10 or int(end_date[1]) < 3:
                    start_date1_should = end_date[0] + '-01'
                else:
                    start_date1_should = 0
                start_date2_should = str((int(end_date[0]) - 1)) + '-' + self.add_zero(str((int(end_date[1]) + 1)))
                start_date3_should = str((int(end_date[0]) - 1)) + '-' + self.add_zero(str((int(end_date[1]) - 1)))

                # if end_date[0] == "2016":
                #     print('-6'*10)
                #     print('end_date')
                #     print(end_date)
                #     print('end_date')
                #     print(start_date_should)
                #     print(start_date0_should)
                #     print(start_date1_should)
                #     print(start_date2_should)
                #     print(start_date3_should)
                #     print(start_date)
                #     print('=5'*10)
                #     print('=6'*10)

                if (not segment) and (identifier.text == entitycentralindexkey) \
                        and (
                        start_date == start_date_should or start_date == start_date0_should or
                        start_date == start_date1_should or start_date == start_date2_should or
                        start_date == start_date3_should):
                    flow_context_id = context['id']

            except Exception as ex:
                # print(ex)
                continue

        # if end_date[0] == "2016":
        #     print('-flow'*20)
        #     print(flow_context_id)
        #     print(documentperiodenddate)
        #     print('-flow'*20)

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
                segment = context.find(context_name[0] + ':segment')
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

        # log_debug("get_data_for_years (after getting matching_accounts): "+dic_data_year[3]+", "+str(dic_data_year[0]))

        # print("Current Time 6 =", datetime.datetime.now().strftime("%H:%M:%S"))

        accounts_flow = {}
        for k in accounts_['flow']:
            accounts_flow[k[0:92]] = accounts_['flow'][k]

        accounts_instant = {}
        for k in accounts_['instant']:
            accounts_instant[k[0:92]] = accounts_['instant'][k]

        # if str(dic_data_year[0]) == "2020":
        #     print(int(dic_data_year[1]['dei']['documentfiscalyearfocus']))
        #     print(str(dic_data_year[0]))
        #     print(accounts_instant)

        for std in used_accounting_standards:
            tag_list = soup.find_all(re.compile(std + ":"))
            for tag in tag_list:
                name_ = tag.name.split(":")
                try:
                    if name_[1][0:92] in accounts_instant and tag['contextref'] == instant_context_id:
                        if accounts_instant[name_[1][0:92]][2] == std:
                            order = accounts_instant[name_[1][0:92]][0]
                            scale = accounts_instant[name_[1][0:92]][1]
                            if scale == 1:
                                year_data[order] = tag.text
                            else:
                                year_data[order] = int(tag.text) / scale
                    if name_[1][0:92] in accounts_flow and tag['contextref'] == flow_context_id:
                        order = accounts_flow[name_[1][0:92]][0]
                        scale = accounts_flow[name_[1][0:92]][1]
                        if scale == 1:
                            year_data[order] = tag.text
                        else:
                            year_data[order] = int(tag.text) / scale

                except Exception as ex:
                    pass
                    # print("Error: year=" + str(dic_data_year[0]) + "   dic=" + dic_data_year[1]['href'] + "   " + str(ex) + tag.text)

        dic_data_year[1]['year_data'] = year_data

        log_debug("End get_data_for_years: " + dic_data_year[3] + ", " + str(dic_data_year[0]))
        # print("Current Time End get data = " + str(dic_data_year[0]), datetime.datetime.now().strftime("%H:%M:%S"))
        return dic_data_year

    def get_dic_company_info_q(self, company, dic_company_info):
        # print('get_dic_company_info_q')
        # print(dic_company_info)
        # for key in dic_company_info['data']:
        #     print(key)
        #     u = dic_company_info['data'][key]
        #     print(u)
        #     u = dic_company_info['data'][key]['href']
        #     print(u)

        # print('get_dic_company_info_q')
        headers = {'User-Agent': 'amos@drbaranes.com'}
        base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&count=100"  # &dateb={}"
        type_ = '10-Q'
        url_q = base_url.format(company.cik, type_)
        # print(url_q)
        dic_data = {'10q_url': url_q, 'data': {}}
        try:
            edgar_resp_q = requests.get(url_q, headers=headers, timeout=30)
        except Exception as ex:
            print(str(ex))
        edgar_str_q = edgar_resp_q.text
        soup_q = BeautifulSoup(edgar_str_q, 'html.parser')
        table_tag_q = soup_q.find('table', class_='tableFile2')
        try:
            rows = table_tag_q.find_all('tr')
        except Exception as ex:
            return dic_company_info

        # print('dic_data 1110000')
        # print(dic_data)
        # print('-'*100)

        for row in rows:
            try:
                cells = row.find_all('td')
                # print(cells[0].text.lower())
                if len(cells) > 3:
                    if cells[0].text.lower() != type_.lower():
                        continue
                    # for filing_year in range(2019, 2020):
                    for filing_year in range(self.xbrl_start_year, self.today_year + 1):
                        if str(filing_year) in cells[3].text:
                            # print('---')
                            m = cells[3].text.split("-")[1]
                            # print(cells[3].text, 'filing_year', filing_year, 'm', m)
                            try:
                                # print('='*20)
                                if filing_year not in dic_data['data']:
                                    dic_data['data'][filing_year] = {}
                            except Exception as exx:
                                print(str(exx))
                            dic_data['data'][filing_year][m] = {'href': 'https://www.sec.gov' + cells[1].a['href']}
            except Exception as ex:
                pass

        # print('dic_data111')
        # print(dic_data)
        # print('='*100)

        for key in dic_data['data']:
            # print(key)
            try:
                # print(dic_company_info['data'][str(key)])
                url_ = dic_company_info['data'][str(key)]['href']
                # print(url_)
                # print("dic_data['data'][key]")
                # print(dic_data['data'][key])
                dic_data['data'][key]['Q4'] = {'href': url_}
            except Exception as ex:
                dic_data['data'][key]['Q4'] = {'href': ""}
                # print("Error 300: " + str(ex))
                log_debug("Error 300: " + str(ex))
            for m in dic_data['data'][key]:
                # print(1111)
                # print('='*150)
                # print(key, m)
                if dic_data['data'][key][m]['href'] == "":
                    # print("empty: "+m)
                    continue
                dic_data = self.get_data_for_one_year_q(key, m, dic_data, dic_company_info)
                # print('='*150)

        # print(dic_data)
        # print('-='*50)
        return dic_data

    def get_data_for_one_year_q(self, key, m, dic_data, dic_company_info):
        # print(key, m)
        value = dic_data['data'][key][m]
        temp = [key, m, value,
                dic_company_info['company_info']['SIC'], dic_company_info['company_info']['ticker'],
                dic_company_info['statements']
                ]
        # print('temp')
        # print(temp)
        d = self.get_data_for_years_q(dic_data_year=temp)[2]
        # print('-d'*50)
        # print(d)
        # print('-d'*50)
        dic_data['data'][key][m] = d
        # print(dic_data)
        return dic_data

    def get_data_for_years_q(self, dic_data_year):
        # print("start get_data_for_years_q: "+dic_data_year[4]+", "+str(dic_data_year[0])+", "+str(dic_data_year[1]))
        # print("start get_data_for_years_q: "+dic_data_year[4]+", "+str(dic_data_year[0])+", "+str(dic_data_year[1]))
        headers = {'User-Agent': 'amos@drbaranes.com'}
        doc_resp = requests.get(dic_data_year[2]['href'], headers=headers, timeout=30)
        doc_str = doc_resp.text
        # print('-'*100)
        # print('-'*100)
        # print("get_data_for_years_q: "+str(dic_data_year[4])+", "+str(dic_data_year[0])+":"+str(dic_data_year[1]),
        #       dic_data_year[2]['href'])

        # Find the XBRL link
        xbrl_link = ''
        soup = BeautifulSoup(doc_str, 'html.parser')
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')
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

            dic_data_year[2]['xbrl_link'] = 'https://www.sec.gov' + xbrl_link
            accession_number = xbrl_link.split('/')
            # print('-12-'*3, 'accession_number', accession_number)

            view_link = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik='
            view_link += accession_number[4] + '&accession_number=' + accession_number[5] + '&xbrl_type=v#'

            r_link = "https://www.sec.gov/Archives/edgar/data/" + accession_number[4] + "/" + accession_number[5] + "/R"
            dic_data_year[2]['r_link'] = r_link
            dic_data_year[2]['view_link'] = view_link
            # print(dic_data_year)
        except Exception as ex:
            return dic_data_year

        xbrl_resp = requests.get(dic_data_year[2]['xbrl_link'], headers=headers, timeout=30)
        xbrl_str = xbrl_resp.text

        # print("get_data_for_years q: "+dic_data_year[4]+", "+str(dic_data_year[0])+":"+str(dic_data_year[1]))
        # print('-'*20)

        soup = BeautifulSoup(xbrl_str, 'lxml')
        dic_data_year[2]['dei'] = {}
        for tag in soup.find_all(re.compile("dei:")):
            name_ = tag.name.split(":")
            dic_data_year[2]['dei'][name_[1]] = tag.text

        documentperiodenddate = dic_data_year[2]['dei']['documentperiodenddate']
        entitycentralindexkey = dic_data_year[2]['dei']['entitycentralindexkey']
        if str(dic_data_year[1]) == "Q4":
            documentfiscalperiodfocus = "Q4"
            dic_data_year[2]['dei']['documentfiscalperiodfocus'] = "Q4"
        else:
            documentfiscalperiodfocus = dic_data_year[2]['dei']['documentfiscalperiodfocus']

        # print(dic_data_year[2]['dei'])
        # print(documentperiodenddate, entitycentralindexkey, documentfiscalperiodfocus)
        # print('-'*20)

        # print("Current Time 4 =", datetime.datetime.now().strftime("%H:%M:%S"))
        flow_context_id = ""
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
                    segment = context.find(context_name[0] + ':segment')
                    startdate = context.find(context_name[0] + ':startdate')
                else:
                    identifier = context.find('identifier')
                    segment = context.find('segment')
                    startdate = context.find('startdate')

                end_date = tag.text.split('-')
                start_date = startdate.text.split('-')
                start_date = start_date[0] + '-' + start_date[1]

                # print(end_date[1])
                if 12 >= int(end_date[1]) > 4:
                    start_date_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 3))
                    start_date0_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 2))
                    start_date1_should = end_date[0] + '-' + self.add_zero(str(int(end_date[1]) - 4))
                    start_date2_should = "none"
                    # print(start_date_should)
                elif int(end_date[1]) <= 4:
                    start_date_should = end_date[0] + '-01'
                    start_date0_should = end_date[0] + '-02'
                    start_date1_should = str((int(end_date[0]) - 1)) + '-12'
                    start_date2_should = str((int(end_date[0]) - 1)) + '-11'

                # if str(dic_data_year[1]) == "Q4":
                #     if end_date[0] == "2021":
                #         print('-6-'*50)
                #         print('end_date')
                #         print(end_date)
                #         print('end_date')
                #         print(start_date_should)
                #         print(start_date0_should)
                #         print(start_date1_should)
                #         print('start_date')
                #         print(start_date)
                #         print('=5'*10)
                #         print('=6'*10)

                if (not segment) and (identifier.text == entitycentralindexkey) \
                        and (start_date == start_date_should or start_date == start_date0_should or
                             start_date == start_date1_should or start_date == start_date2_should):
                    flow_context_id = context['id']

            except Exception as ex:
                # print(ex)
                continue

        # if end_date[0] == "2021" or end_date == "2020":
        #     print('-flow'*20)
        #     print(documentfiscalperiodfocus)
        #     print(end_date)
        #     print(flow_context_id, documentperiodenddate, start_date_should)
        #     print('-flow'*20)

        # print('-'*50)

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
                segment = context.find(context_name[0] + ':segment')
            else:
                identifier = context.find('identifier')
                segment = context.find('segment')
            if not segment and identifier.text == entitycentralindexkey:
                # print(context)
                instant_context_id = context['id']

        # if end_date[0] == "2021":
        #     print('-instant'*10)
        #     print(instant_context_id)
        #     print(documentperiodenddate)
        #     print('-instant'*10)

        # temp = [key, m, value,
        #         dic_company_info['company_info']['SIC'], dic_company_info['company_info']['ticker'],
        #         dic_company_info['statements']
        #         ]

        # print(dic_data_year[4], int(dic_data_year[2]['dei']['documentfiscalyearfocus']), dic_data_year[3], dic_data_year[5])

        matching_accounts, accounts_, used_accounting_standards = \
            self.get_matching_accounts(dic_data_year[4], int(dic_data_year[2]['dei']['documentfiscalyearfocus']),
                                       dic_data_year[3], dic_data_year[5])

        # print(222222222222222222222)
        dic_data_year[2]['matching_accounts'] = matching_accounts
        # print(matching_accounts)
        # print(3333333333333333333)
        year_data = {}
        # log_debug("get_data_for_years (after getting matching_accounts): "+dic_data_year[3]+", "+str(dic_data_year[0]))
        # print("Current Time 6 =", datetime.datetime.now().strftime("%H:%M:%S"))
        accounts_flow = {}
        for k in accounts_['flow']:
            accounts_flow[k[0:92]] = accounts_['flow'][k]

        accounts_instant = {}
        for k in accounts_['instant']:
            accounts_instant[k[0:92]] = accounts_['instant'][k]

        # if str(dic_data_year[0]) == "2021":
        #     print(int(dic_data_year[2]['dei']['documentfiscalyearfocus']))
        #     print(str(dic_data_year[0]))
        #     print(accounts_instant)

        for std in used_accounting_standards:
            tag_list = soup.find_all(re.compile(std + ":"))
            for tag in tag_list:
                name_ = tag.name.split(":")
                try:
                    if name_[1][0:92] in accounts_instant and tag['contextref'] == instant_context_id:
                        if accounts_instant[name_[1][0:92]][2] == std:
                            order = accounts_instant[name_[1][0:92]][0]
                            scale = accounts_instant[name_[1][0:92]][1]
                            if scale == 1:
                                year_data[order] = tag.text
                            else:
                                year_data[order] = int(tag.text) / scale
                    if name_[1][0:92] in accounts_flow and tag['contextref'] == flow_context_id:
                        order = accounts_flow[name_[1][0:92]][0]
                        scale = accounts_flow[name_[1][0:92]][1]
                        if scale == 1:
                            year_data[order] = tag.text
                        else:
                            year_data[order] = int(tag.text) / scale

                except Exception as ex:
                    pass
                    # print("Error: year=" + str(dic_data_year[0]) + "   dic=" + dic_data_year[1]['href'] + "   " + str(ex) + tag.text)

        # print(year_data)
        # print(4444444444444444444)

        dic_data_year[2]['year_data'] = year_data

        log_debug("End get_data_for_years: " + dic_data_year[3] + ", " + str(dic_data_year[0]))
        # print("Current Time End get data = " + str(dic_data_year[0]), datetime.datetime.now().strftime("%H:%M:%S"))
        return dic_data_year

    # to be deleted --
    def get_matching_accounts(self, ticker, year, sic, statements):
        try:
            if year <= self.xbrl_base_year:
                years = sorted(range(year, self.xbrl_base_year + 1), reverse=True)
            else:
                years = range(self.xbrl_base_year, year + 1)
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

        # print('dic_matches 0')
        # print(year)
        # print(dic_matches)
        # print('dic_matches 0')

        for y in years:
            for m in matches:
                if m.year == y:
                    dic_matches[m.account.order] = [m.match_account, m.accounting_standard]
                    if m.accounting_standard not in used_accounting_standards:
                        used_accounting_standards.append(m.accounting_standard)

        # print('dic_matches')
        # print(year)
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

                try:
                    if int(a_order) in dic_matches:
                        ma_, ma_std = dic_matches[int(a_order)][0].lower(), dic_matches[int(a_order)][1].lower()
                    else:
                        ma_, ma_std = "", ""
                except Exception as ex:
                    pass
                    # print('ex')
                    # print(ex)

                if ma_ != '':
                    if statements[st_]['accounts'][a_order][1] == 1:
                        accounts_['instant'][ma_] = (a_order, statements[st_]['accounts'][a_order][2], ma_std)
                    else:
                        accounts_['flow'][ma_] = (a_order, statements[st_]['accounts'][a_order][2], ma_std)
                matching_accounts[a_order] = [ma_, ma_std]

        # print('matching_accounts')
        # print(year)
        # print(matching_accounts)
        # print('matching_accounts')

        return matching_accounts, accounts_, used_accounting_standards

    def save_industry_default(self, year, ticker, sic):
        dic = {'status': 'ok'}
        if year == self.xbrl_base_year:
            # print('-1'*20)
            industry = XBRLIndustryInfo.objects.get(sic_code=sic)
            c, created = XBRLCompanyInfo.objects.get_or_create(industry=industry, company_name=sic, ticker=sic, cik=sic)
            try:
                # print('-2'*20)
                # zero_company = XBRLValuationAccountsMatch.objects.filter(Q(company__ticker=ticker) & Q(year=year)).all()
                # zero_company.update(company=c, year=0)
                for m in XBRLValuationAccountsMatch.objects.filter(Q(company__ticker=ticker) & Q(year=year)).all():
                    cs, created_s = XBRLValuationAccountsMatch.objects.get_or_create(year=0, company=c,
                                                                                     account=m.account)
                    if created_s:
                        cs.match_account = m.match_account
                        cs.accounting_standard = m.accounting_standard
                        cs.save()
                        m.delete()
            except Exception as ex:
                print(ex)
                dic = {'status': 'ko'}
        else:
            dic = {'status': 'You can update only data of year 2020.'}
        return dic

    # # #
    # Functions for Forecasted EPS
    def get_sp500(self):
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.sp_tickers = list(pd.read_html(sp500_url)[0]['Symbol'].values)
        self.sp_tickers = [x.split('.')[0] for x in self.sp_tickers]
        for ticker in self.sp_tickers:
            try:
                XBRLCompanyInfo.objects.get(ticker=ticker)
            except Exception as ex:
                try:
                    dic = self.create_company_by_ticker(ticker=ticker)
                except Exception as exx:
                    self.sp_tickers.remove(ticker)
                    # print('exx')
                    # print(exx)

        dic = {'status': 'ok', 'sp_tickers': self.sp_tickers}
        log_debug("End load_sp_returns.")
        return dic

    def month_to_num(self, month):
        return {
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
        }[month]

    def add_zero(self, s):
        if len(s) == 1:
            s = "0" + s
        return s

    def upload_old_earning_forecast_sp500(self):
        # XBRLSPEarningForecast.truncate()
        # print('upload_old_earning_forecast_sp500')
        sp_tickers = self.get_sp500()['sp_tickers']
        for ticker_ in sp_tickers:
            # print(ticker_)
            try:
                company_ = XBRLCompanyInfo.objects.get(ticker=ticker_)
                s, c = XBRLSPStatistics.objects.get_or_create(company=company_)
            except Exception as eex:
                pass
                # print("error sp_tickers: 111" + ticker_ + " : " + str(eex))
        # print("End check sp500")
        for file in os.listdir(self.TEXT_PATH):
            # log_debug("Start Processing file: " + file)
            # print(file)
            log_debug("Start file: " + file +" wait for it to finish/")
            file_path = f"{self.TEXT_PATH}/{file}"
            with open(file_path, 'r') as f:
                text = f.read()
                soup = BeautifulSoup(text, 'html.parser')
                rows = soup.find_all('tr')
                for row in rows:
                    try:
                        cells = row.find_all('td')
                        if len(cells) < 3:
                            dd = cells[0].text.split(",")
                            ddd = dd[1].strip().split(" ")
                            mm = self.month_to_num(ddd[0])
                            yy = dd[2].strip()
                            dd = ddd[1]
                            date_str = yy + "-" + mm + "-" + self.add_zero(dd)
                            date_ = parse_date(date_str)
                        else:
                            # if cells[2].text != '--':

                            ticker = cells[1].find('a').text
                            # print(ticker)
                            if ticker in sp_tickers:
                                # print('-'*20)
                                # print('in sp')
                                # print(date_str)
                                # print(ticker)
                                # log_debug("Ticker: " + ticker)
                                # print('-'*5)
                                actual = cells[2].text
                                forecast = cells[3].text.split('/')[1].lstrip()
                                # print("actual: " + str(actual) + " forecast: " + str(forecast))
                                # print('-'*20)

                                company = XBRLCompanyInfo.objects.get(ticker=ticker)
                                year = date_.year
                                quarter = math.ceil(date_.month / 3)
                                ef, ct = XBRLSPEarningForecast.objects.get_or_create(company=company, year=year,
                                                                                     quarter=quarter)
                                # print(ct)
                                # print(ef)
                                # print("Got or created record")
                                # print('-'*20)
                                try:
                                    forecast_ = float(forecast)
                                    ef.forecast = forecast_
                                    ef.save()
                                    # print("forecast saved")
                                except Exception as eex:
                                    # print("error forecast 123: " + str(eex))
                                    pass

                                try:
                                    actual_ = float(actual)
                                    ef.actual = actual_
                                    ef.save()
                                    # print("Actual saved")
                                except Exception as eex:
                                    # print("error actual 234: " + str(eex))
                                    ef.actual = None
                                    # pass

                                try:
                                    ef.date = date_
                                    ef.save()
                                    # print("Date saved")
                                except Exception as eex:
                                    pass
                                    # print("error Date act for 444: " + str(eex))

                                # try:
                                #     ef.save()
                                # except Exception as eex:
                                #     pass
                                #     # print("error Save act for: " + str(eex))

                                # print('ticker1')
                                try:
                                    self.get_ticker_prices(earning_forecast=ef)
                                except Exception as eex:
                                    pass
                                    # print("error Price act for 555: " + str(eex))

                                try:
                                    next_release_date = self.get_next_relealse_date(cells[1], date_)
                                    # print(next_release_date)
                                    ef.next_release_date = next_release_date
                                    s = XBRLSPStatistics.objects.get(company__ticker=ticker)
                                    s.next_release_date = next_release_date
                                    s.save()
                                    ef.save()
                                    # print("next_release_date saved")
                                except Exception as eex:
                                    pass
                                    # print("error next_release_date: " + str(eex))

                                # print(ticker)
                                # print('ticker2')

                                try:
                                    company.company_statistic.set_company_statistics()
                                except Exception as eex:
                                    pass
                                    # print("error company.set_company_statisitcs 666: " + str(eex))
                    except Exception as ex:
                        # if ticker in sp_tickers:
                        # print('ex')
                        # print(ex)
                        # print(ticker)
                        # print(cells[2].text)
                        # print('ex')
                        pass
            print("End Processing file: " + file)
            log_debug("End Processing file: " + file)
        log_debug("End Processing all files1: ")
        log_debug("End Processing all files2: ")

    def get_next_relealse_date(self, cell, date):
        # print("get_next_relealse_date ")
        # print("get_next_relealse_date ")
        # print("get_next_relealse_date ")
        # print(cell)
        # print(cell.find('a'))
        # print(cell.find('a')['href'])
        url = cell.find('a')['href']
        url = "https://www.investing.com/" + url
        # print(url)
        id_ = "earningsHistory" + cell['_r_pid']
        # print(id_)
        headers = {'User-Agent': 'amos@drbaranes.com'}
        sp_resp = requests.get(url, headers=headers, timeout=30)
        sp_str = sp_resp.text
        soup = BeautifulSoup(sp_str, 'html.parser')
        table_tag = soup.find('table', id=id_)
        # print(table_tag)
        tbody_tag = table_tag.find('tbody')
        # print("-"*100)
        # print(date)
        # print("-"*10)
        try:
            # date_str = tbody_tag.find_all('tr')[0]['event_timestamp']
            next_date = datetime.datetime.now()
            next_date = (next_date + timedelta(days=180)).date()
            # print(next_date)
            for k in tbody_tag.find_all('tr'):
                date_str = k['event_timestamp']
                # print(date_str)
                date_ = parse_date(date_str)
                if date < date_ < next_date:
                    next_date = date_
                # print("-"*5)
        except Exception as ex:
            print("Error 105" + str(ex))
        # print(next_date)
        # print("-"*100)

        return next_date

    def get_earning_forecast_sp500(self):
        # print('get_earning_forecast_sp500')
        sp_tickers = self.get_sp500()['sp_tickers']
        for ticker_ in sp_tickers:
            try:
                # print(ticker_)
                company_ = XBRLCompanyInfo.objects.get(ticker=ticker_)
                # print(company_)
                s, c = XBRLSPStatistics.objects.get_or_create(company=company_)
                # print(c)
            except Exception as eex:
                pass
                # print("error 345 sp_tickers: " + ticker_ + " : " + str(eex))
        headers = {'User-Agent': 'amos@drbaranes.com'}
        url = "https://www.investing.com/earnings-calendar/"
        sp_resp = requests.get(url, headers=headers, timeout=30)
        # print("Current Time 11 =", datetime.datetime.now().strftime("%H:%M:%S"))
        sp_str = sp_resp.text
        soup = BeautifulSoup(sp_str, 'html.parser')
        form_tag = soup.find('form', id='earningsCalendarForm')
        # print(form_tag)
        form_cells = form_tag.find_all('input')
        # print(form_cells)
        date_str = form_cells[0]['value']
        date_ = parse_date(date_str)

        table_tag = soup.find('table', id='earningsCalendarData')
        tbody_tag = table_tag.find('tbody')
        try:
            rows = tbody_tag.find_all('tr')
            for row in rows:
                try:
                    cells = row.find_all('td')
                    # print(row)
                    if len(cells) > 3:
                        # print('row 3')
                        # if cells[2].text != '--':
                        ticker = cells[1].find('a').text
                        # print(ticker)
                        if ticker in sp_tickers:
                            # print('ticker in sp')
                            # print(ticker)
                            year = date_.year
                            quarter = math.ceil(date_.month / 3)
                            company = XBRLCompanyInfo.objects.get(ticker=ticker)
                            ef, ct = XBRLSPEarningForecast.objects.get_or_create(company=company, year=year,
                                                                                 quarter=quarter)
                            if cells[2].text != '--':
                                actual = cells[2].text
                                forecast = cells[3].text.split('/')[1].lstrip()
                                ef.forecast = forecast
                                ef.actual = actual
                                ef.date = date_
                                next_release_date = self.get_next_relealse_date(cells[1], date_)
                                ef.next_release_date = next_release_date
                                ef.save()
                                s, c = XBRLSPStatistics.objects.get_or_create(company__ticker=ticker)
                                s.next_release_date = next_release_date
                                s.save()
                                self.get_ticker_prices(ef)
                                try:
                                    company.company_statistic.set_company_statistics()
                                except Exception as eex:
                                    pass
                                    # print("error company.set_company_statisitcs: " + str(eex))
                except Exception as ex:
                    print("error 102: " + str(ex))
        except Exception as ex:
            return print("Error 101")
        dic = {'status': 'ok'}
        return dic

    def get_announcement_time_day(self, s_day):
        try:
            s_from = "2021-01-01"
            s_to = "2021-12-31"
            url = "https://finance.yahoo.com/calendar/earnings?from=" + s_from + "&to=" + s_to + "&day=" + s_day
            log_debug(url)
            headers = {'User-Agent': 'amos@drbaranes.com'}
            sp_resp = requests.get(url, headers=headers, timeout=30)
            sp_str = sp_resp.text
            # print(sp_str)
            soup = BeautifulSoup(sp_str, 'html.parser')
            id_ = "cal-res-table"
            div_tag = soup.find('div', id=id_)
            # print('--12--')
            tbody_tag = div_tag.find('tbody')
            # print('--13--')
            # print("-"*100)
            # print(tbody_tag)
            # print("-"*10)
            sp_tickers = self.get_sp500()['sp_tickers']
            rows = tbody_tag.find_all('tr')
            # print('--14--')
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        sa = ""
                        # print(cells[2])
                        sa_ = cells[2].text
                        if sa_ == "Time Not Supplied":
                            sa = "N"
                        elif sa_ == "TAS":
                            sa = "T"
                        elif sa_ == "Before Market Open":
                            sa = "B"
                        elif sa_ == "After Market Close":
                            sa = "A"
                        else:
                            sa = "O"
                        ticker = cells[0].find('a').text
                        if ticker in sp_tickers:
                            # log_debug(ticker +":" + sa_ + ":" + sa)
                            s = XBRLSPStatistics.objects.get(company__ticker=ticker)
                            s.announcement_time = sa
                            s.save()
                            log_debug("Saved: " + ticker + " : " + sa)
                except Exception as ex:
                    log_debug("Error 102: " + ticker + " : " + str(ex))
        except Exception as ex:
            log_debug("Error 101: " + str(ex))

    def get_announcement_time(self, m=""):
        try:
            m = int(m)
            nd = 31
            if m in [1, 3, 5, 7, 8, 10, 12]:
                nd = 32
            elif m == 2:  # do not care about 29
                nd = 28
            sm = self.add_zero(str(m))
            for d in range(1, nd):
                sd = self.add_zero(str(d))
                s_day = "2021-" + sm + "-" + sd
                # print(s_day)
                log_debug("Start day: " + s_day)
                # print('-----------')
                try:
                    self.get_announcement_time_day(s_day=s_day)
                except Exception as ex:
                    log_debug("Error 202 time: " + str(ex))
            # print(s_day)
            # self.get_announcement_time_day(s_day="2021-07-20")
        except Exception as ex:
            log_debug("Error 201 time: " + str(ex))
        dic = {'status': 'ok'}
        return dic

    def get_ticker_prices(self, earning_forecast):
        # https://pypi.org/project/yahoofinancials/
        # https://www.analyticsvidhya.com/blog/2021/06/download-financial-dataset-using-yahoo-finance-in-python-a-complete-guide/

        # print(earning_forecast.company.ticker)
        yahoo_financials = YahooFinancials(earning_forecast.company.ticker)
        today = earning_forecast.date
        # print(today)
        yesterday = (today + timedelta(days=-1))
        # print(yesterday)
        today_str = str(today)
        yesterday_str = str(yesterday)
        data = yahoo_financials.get_historical_price_data(start_date='2015-01-01',
                                                          end_date=str(today + timedelta(days=1)),
                                                          time_interval='daily')
        # print(data)
        df = pd.DataFrame(data[earning_forecast.company.ticker]['prices'])
        df = df.drop('date', axis=1).set_index('formatted_date')
        # print(df.tail())
        try:
            today_price = int(100 * df.filter(items=[today_str], axis=0)['adjclose']) / 100
            # print(today_price)
            earning_forecast.today_price = today_price
        except Exception as ex:
            pass
            # print('ex 1')
            # print(ex)
        is_ok = False
        while not is_ok:
            try:
                yesterday_price = int(100 * df.filter(items=[yesterday_str], axis=0)['adjclose']) / 100
                # print(yesterday_price)
                earning_forecast.yesterday_price = yesterday_price
                is_ok = True
            except Exception as ex:
                yesterday = (yesterday + timedelta(days=-1))
                # print(yesterday)
                yesterday_str = str(yesterday)
                # print('ex 2')
                # print(ex)
        earning_forecast.save()
        dic = {'status': 'ok'}
        return dic

    # Should delete this function
    def get_earning_forecast_sp500_view(self):
        d = {}
        for t in XBRLSPEarningForecast.objects.all():
            if t.company.ticker not in d:
                d[t.company.ticker] = {}
            new_ticker = False
            if t.year not in d[t.company.ticker]:
                d[t.company.ticker][t.year] = {}
                new_ticker = True
            if t.quarter not in d[t.company.ticker][t.year]:
                d[t.company.ticker][t.year][t.quarter] = ['f', 'a', 'p', '-p']
            d[t.company.ticker][t.year][t.quarter][0] = str(t.forecast)
            d[t.company.ticker][t.year][t.quarter][1] = str(t.actual)
            d[t.company.ticker][t.year][t.quarter][2] = str(t.today_price)
            d[t.company.ticker][t.year][t.quarter][3] = str(t.yesterday_price)
            if new_ticker:
                d[t.company.ticker][t.year][t.quarter].append(str(t.next_release_date))

        # print(d)
        return {'status': 'ok', 'earning_forecast_sp500_view': d}

    def get_earning_forecast_sp500_view_main_detail(self, ticker):
        # print(ticker)
        d = {}
        for r in XBRLSPEarningForecast.objects.filter(company__ticker=ticker).order_by('-year', 'quarter').all():
            try:
                d[str(int(r.year) * 10 + int(r.quarter))] = [r.year, r.quarter, float(r.forecast), float(r.actual),
                                                             float(r.today_price), float(r.yesterday_price)]
            except Exception as ex:
                pass
                # print('error get_earning_forecast_sp500_view_main')
                # print(ex)
        # print(d)
        return {'status': 'ok', 'get_earning_forecast_sp500_view_main_detail': d}

    def get_earning_forecast_sp500_view_main(self, order_by):
        # print('get_earning_forecast_sp500_view_main')
        # print('order_by')
        # print(order_by)
        # print('order_by')

        d = {}
        for t in XBRLSPStatistics.objects.select_related("company__industry__main_sic").order_by(order_by).all():
            if t.company.ticker not in d:
                try:
                    d[str(t.company.ticker)] = {"cn": str(t.company.company_name), "nrd": str(t.next_release_date),
                                                "mapc": str(t.mean_abs_price_change),
                                                "maafc": str(t.mean_abs_actual_forecast_change),
                                                "maafcm": str(t.mean_abs_actual_forecast_change_money),
                                                "cafp": str(t.correlation_afp),
                                                "ud": str(t.updated),
                                                "sic": t.company.industry.sic_code,
                                                "msic": t.company.industry.main_sic.sic_code,
                                                "bfp": str(t.butterfly_price),
                                                "stp": str(t.straddle_price),
                                                "a": str(t.announcement_time)}
                except Exception as ex:
                    print('error get_earning_forecast_sp500_view_main')
                    print(ex)
        # print(d)
        return {'status': 'ok', 'earning_forecast_sp500_view_main': d}

    # # #
    #  Data processing
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

                company, created = XBRLCompanyInfo.objects.get_or_create(industry=industry_, ticker=ticker, cik=cik0,
                                                                         company_name=company_name_,
                                                                         company_letter=company_name_[0].upper())
                company_id = company.id

        except Exception as ex:
            pass
            # print('error 108: '+str(ex))
        return {'status': 'ok', 'id': company_id, 'company_name': company_name_}

    def get_companies_for_exchange(self, exchange, exchange_url):
        companies = pd.DataFrame(columns=['exchange', 'name', 'ticker', 'letter'])
        company_name = []
        company_ticker = []
        company_letter = []
        letters = string.ascii_uppercase
        for letter in letters:
            company_name, company_ticker, company_letter = self.get_companies_for_letter(
                letter, exchange_url + letter, company_name, company_ticker, company_letter)
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
    #

    # general purpose functions for testing
    def test(self):
        try:
            today_ = datetime.datetime.today()
            nday = today_.weekday()  # Monday = 0
            h = today_.hour
            m = today_.minute
            log_debug(str(nday)+" : "+str(h)+" : "+str(m))

            data = ()
            ssql = " insert into corporatevaluation_XBRLRealEquityPricesArchive(ticker,t,o,h,l,c,v) "
            ssql += "select ticker,t,o,h,l,c,v from corporatevaluation_XBRLRealEquityPrices"
            # print(ssql)

            count = SQL().exc_sql(ssql, data)
            # print(count)
            XBRLRealEquityPrices.truncate()

        except Exception as ex:
            print("Error200: "+str(ex))
            pass
        result = {'status': "ok"}
        return result

    def test1(self):
        XBRLRealEquityPrices.truncate()
        result = {'status': "ok"}
        return result

    def test2(self):
        XBRLRealEquityPricesArchive.truncate()
        result = {'status': "ok"}
        return result

#   --- Stage 1 get list of companies ---
    def set_sic_code(self):
        log_debug("Start set_sic_code")
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
        log_debug("End set_sic_code")
        return {'status': 'ok'}

    def get_all_companies(self):
        log_debug("Start get_all_companies")
        exchanges = {
            'nyse': 'nyse/newyorkstockexchange',
            'nasdaq': 'nasdaq/nasdaq',
            'amex': 'amex/americanstockexchange'}

        # writer = pd.ExcelWriter(self.EXCEL_PATH+'/all_companies.xlsx', engine='xlsxwriter')
        n = 0
        companies = None
        for exchange in exchanges:
            # print(exchange)
            url = 'https://www.advfn.com/' + exchanges[exchange] + '.asp?companies='
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
            print("Error 107:  " + str(ex))

        # print('done collecting data on companies')

        try:
            # print(companies)
            for i, c in companies.iterrows():
                # print(c)
                # print(c['exchange'])
                # print(c['name'])

                # print(c['ticker'])

                # print(c['letter'])
                a, created = XBRLCompanyInfoInProcess.objects.get_or_create(exchange=c['exchange'],
                                                                            company_name=c['name'],
                                                                            ticker=c['ticker'],
                                                                            company_letter=c['letter'])
        except Exception as ex:
            print("Error 2:  " + str(ex))

        # print('done loading data to XBRLCompanyInfoInProcess')

        # self.companies.reset_index(drop=True, inplace=True)
        # self.companies.to_excel(writer, sheet_name='all')
        # writer.save()
        log_debug("End get_all_companies")
        dic = {'status': 'ok'}
        return dic

    def clean_data_for_all_companies(self):
        log_debug("Start clean_data_for_all_companies")
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
                # print('error 106: '+str(ex))
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
                        for filing_year in range(self.xbrl_start_year, self.today_year + 1):
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
        log_debug("End clean_data_for_all_companies")
        return {'status': 'ok'}

    def copy_processed_companies(self):
        log_debug("Start copy_processed_companies")
        companies_ = XBRLCompanyInfoInProcess.objects.filter(is_error=False).all()
        for c in companies_:
            try:
                # print(c.ticker)
                i_ = XBRLIndustryInfo.objects.get(sic_code=c.sic)
                XBRLCompanyInfo.objects.get_or_create(industry=i_, exchange=c.exchange, company_name=c.company_name,
                                                      ticker=c.ticker, company_letter=c.company_letter, cik=c.cik)
            except Exception as exc:
                print(str(exc))
        log_debug("End copy_processed_companies")
        dic = {'status': 'ok'}
        return dic

#   --- Stage 2 Regions, countries, ----
    def load_tax_rates_by_country_year(self):
        dic = {'status': 'ko'}
        log_debug("Start load_tax_rates_by_country_year.")
        url = "https://files.taxfoundation.org/20210125115215/io1980-2020-Corporate-Tax-Rates-Around-the-World.csv.xlsx"
        file = "world_taxes"
        self.download_excel_file(url, file)
        df = self.load_excel_data(file)

        XBRLCountryYearData.truncate()
        XBRLCountry.truncate()
        XBRLRegion.truncate()
        log_debug("tables XBRLCountryYearData, XBRLCountry, XBRLRegion were cleaned.")

        for i, r in df.iterrows():
            try:
                region, c = XBRLRegion.objects.get_or_create(name=r['continent'])
                # log_debug('created region: ' + str(r['continent']))
            except Exception as ex:
                log_debug("Error 1 creating region: " + str(r['continent']) + " " + str(ex))

            oecd = True if int(r['oecd']) > 0 else False
            eu27 = True if int(r['eu27']) > 0 else False
            gseven = True if int(r['gseven']) > 0 else False
            gtwenty = True if int(r['gtwenty']) > 0 else False
            brics = True if int(r['brics']) > 0 else False

            try:
                country, c = XBRLCountry.objects.get_or_create(region=region, name=r['country'], iso_2=r['iso_2'],
                                                               iso_3=r['iso_3'], oecd=oecd, gseven=gseven, eu27=eu27,
                                                               gtwenty=gtwenty, brics=brics)
                # log_debug("Created country: " + str(r['continent']) + " " + str(r['country']))
            except Exception as ex:
                log_debug("Error 1 get country: " + str(r['continent']) + " " + str(r['country']) + " " + str(ex))

            d, c = XBRLCountryYearData.objects.get_or_create(country=country, year=int(r['year']))

            if not pd.isna(r['rate']):
                d.tax_rate = round(r['rate'], 2)

            if not pd.isna(r['gdp']):
                d.gdp = round(r['gdp'], 5)

            try:
                d.save()
                log_debug("Done: " + str(r['continent']) + " " + str(r['country']) + " " + str(r['year']))
            except Exception as ex:
                log_debug("Error 2 save country: " + str(r['continent']) + " " + str(r['country']) + " " + str(
                    r['year']) + " " + str(ex))

        dic['status'] = 'ok'
        log_debug("End load_tax_rates_by_country_year.")
        return dic

    def load_country_premium(self, request):
        log_debug("Start load_country_premium.")
        # print('in object load_country_premium(request)')
        match = {'Czech Republic': 'Czechia',
                 'Moldova': 'Republic of Moldova',
                 'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
                 'Jersey (States of)': 'Jersey',
                 'Guernsey (States of)': 'Guernsey',
                 'Bolivia': 'Bolivia (Plurinational State of)',
                 "Côte d'Ivoire": "Cote d'Ivoire",
                 'Democratic Republic of Congo': 'Democratic Republic of the Congo',
                 'Congo (Democratic Republic of)': 'Democratic Republic of the Congo',
                 'Korea': 'Republic of Korea',
                 'Bolivia(Plurinational State of)': 'Bolivia (Plurinational State of)',
                 'United Kingdom of Great Britain and NorthernIreland': 'United Kingdom of Great Britain and Northern Ireland'}
        file = "ctrypremJuly21"
        df = self.load_excel_data(file, sheet_name="Data1")
        # load country and regions
        name_list = [x for x in df['name'].unique() if str(x) != 'nan']
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
                        # log_debug("load_country_premium : updated " + str(c['name']))
                    except Exception as ex:
                        log_debug("Error load_country_premium 10: " + str(c['name']) + " " + str(ex))
                    z = 1
                try:
                    if c['Country'] in match:
                        s_country = match[c['Country']]
                    else:
                        s_country = c['Country']

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
                        # log_debug("load_country_premium : updated country " + str(c['name']) + " " + c['Country'])
                except Exception as ex:
                    log_debug("Error load_country_premium 100: " + str(ex))
        # print('--SP Moodys and tax rates for 2020')
        # log_debug('--SP Moodys and tax rates for 2020')
        for i, c in df.iterrows():
            s_country_ = 'Country1'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            try:
                if not s_country:
                    break
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
                # log_debug("data added for: " + s_country)
            except Exception as ex:
                print('Error 222: for ' + str(ex))
                log_debug("Error load_country_premium 101: " + s_country + " " + str(ex))
        # log_debug('-- End SP Moodys and tax rates for 2020')

        # print('--composite_risk_rating_7_21 --')
        # log_debug('--composite_risk_rating_7_21 --')

        for i, c in df.iterrows():
            s_country_ = 'Country2'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            # print(c)

            s_country = str(s_country)
            if s_country == 'nan':
                break
            try:
                country, created = XBRLCountry.objects.get_or_create(name=s_country)
                data, created = XBRLCountryYearData.objects.get_or_create(country=country, year=2020)
                data.composite_risk_rating = c['composite_risk_rating_7_21']
                data.save()
                # print(data)
                # log_debug("composite_risk_rating_7_21 data added for: " + s_country)
            except Exception as ex:
                print(ex)
                log_debug("Error load_country_premium 102: " + s_country + " " + str(ex))

        # print('-- CDS_07_01_20211 --')
        # log_debug('-- CDS_07_01_20211 --')
        for i, c in df.iterrows():
            s_country_ = 'Country3'
            if c[s_country_] in match:
                s_country = match[c[s_country_]]
            else:
                s_country = c[s_country_]
            # print(s_country)
            # print(c)
            s_country = str(s_country)
            if s_country == 'nan':
                break

            try:
                country = XBRLCountry.objects.filter(name=s_country).all()[0]
                data, created = XBRLCountryYearData.objects.get_or_create(country=country, year=2020)

                # need to consider this.  Since three country with missing data turned to 0.
                if str(c['CDS_01_01_2021']) == 'nan':
                    s_ = 0
                else:
                    s_ = 100 * c['CDS_01_01_2021']
                data.cds = s_
                data.save()
                # print(data.cds)
                # log_debug("CDS_07_01_20211 data added for: " + s_country)
            except Exception as ex:
                log_debug("Error load_country_premium 102: " + s_country + " " + str(ex))

        # print('-- SPMoodys 1--')
        # log_debug('-- SPMoodys 1--')
        XBRLSPMoodys.truncate()
        for i, c in df.iterrows():
            try:
                if str(c['sp_moodys_year']) != 'nan':
                    d, created = XBRLSPMoodys.objects.get_or_create(year=c['sp_moodys_year'], sp=c['SP'],
                                                                    moodys=c['Moodys'])
            except Exception as ex:
                pass

        # print('-- SPMoodys 2--')
        # log_debug('-- SPMoodys 2--')
        for i, c in df.iterrows():
            try:
                if str(c['Rating']) != 'nan':
                    d, created = XBRLSPMoodys.objects.get_or_create(year=int(c['rating_year']), moodys=c['Rating'])
                    dd = round(c['Default_Spread_1_1_2021'] / 100, 2)
                    d.default_spread = dd
                    d_from = round(100 * c['score_from'], 2) / 100
                    d_to = round(100 * c['score_to'], 2) / 100
                    d.score_from = d_from
                    d.score_to = d_to
                    d.save()
                    # log_debug("CDS_07_01_20211 data added for: " + str(c['rating_year']) + " " + str(c['Rating']))
            except Exception as ex:
                log_debug("Error load_country_premium 104: " + str(c['Rating']) + str(ex))

        today = datetime.date.today()
        today = datetime.date(today.year, today.month, today.day)
        today_5 = str(datetime.date(today.year - 5, today.month, today.day))
        today = str(today)
        # print(today)
        # print(today_5)
        s_baml = "https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=BAMLEMPBPUBSICRPIEY&scale=left&cosd=" + today_5 + "&coed=" + today + "&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-09-17&revision_date=2021-09-17&nd=1998-12-31"
        s_bmi = "http://www.spglobal.com/spdji/en/idsexport/file.xls?hostIdentifier=48190c8c-42c4-46af-8d1a-0cd5db894797&redesignExport=true&languageId=1&selectedModule=PerformanceGraphView&selectedSubModule=Graph&yearFlag=fiveYearFlag&indexId=5457901"
        path_baml = self.download_excel_file(s_baml, "baml", ext='xls')
        path_bmi = self.download_excel_file(s_bmi, "bmi", ext='xls')
        try:
            wb_baml = xlrd.open_workbook(path_baml)
            wb_bmi = xlrd.open_workbook(path_bmi)
        except Exception as ex:
            print(ex)

        # log_debug('-- Downloaded baml bmi --')
        sh_bmi = wb_bmi.sheet_by_index(0)
        data_bmi = []
        z = 0
        for cur_row in range(0, sh_bmi.nrows):
            cell = sh_bmi.cell(cur_row, 0)
            # print(cell.value)
            try:
                if 'Effective date' in cell.value:
                    z = 1
                    continue
            except Exception as ex:
                pass
            if cell.value == '':
                z = 0
            if z == 1:
                data_bmi.append(sh_bmi.cell(cur_row, 1).value)
        # print('data_bmi')
        # print(data_bmi)
        data_bmi = [x2 / x1 - 1 for (x1, x2) in zip(data_bmi, data_bmi[1:])]
        std_bmi = statistics.pstdev(data_bmi) * (260 ** 0.5)
        # log_debug('-- Processed file bmi --')
        sh_baml = wb_baml.sheet_by_index(0)
        data_baml = []
        z = 0
        for cur_row in range(0, sh_baml.nrows):
            cell = sh_baml.cell(cur_row, 0)
            # print(cell.value)
            try:
                if 'observation' in cell.value:
                    z = 1
                    continue
            except Exception as ex:
                pass
            if cell.value == '':
                z = 0
            if z == 1:
                data_baml.append(sh_baml.cell(cur_row, 1).value)
        data_baml = [x for x in data_baml if x is not None]
        k1 = 0
        for i in range(len(data_baml)):
            if data_baml[i] == 0:
                data_baml[i] = k1
            k1 = data_baml[i]
        std_baml = statistics.pstdev(data_baml)
        mean_baml = statistics.mean(data_baml)
        cv = std_baml / mean_baml
        volatility_ratio = std_bmi / cv

        # log_debug('-- Processed file baml --')

        # ll = [volatility_ratio, std_bmi, cv, std_baml, mean_baml]
        # print(ll)
        project = Project.objects.filter(translations__language_code=get_language()).get(
            id=int(request.session['cv_project_id']))
        project.volatility_ratio = volatility_ratio
        project.save()
        dic = {'status': 'ok', 'volatility_ratio': volatility_ratio}
        log_debug("End load_country_premium.")
        return dic

    def update_region_risk_premium(self, request):
        project = Project.objects.filter(translations__language_code=get_language()).get(
            id=request.session['cv_project_id'])
        XBRLCountryYearData.project = project
        XBRLRegionYearData.project = project
        for r in XBRLRegion.objects.filter(updated_adamodar=True).all():
            # print('-------')
            # print(r)
            ltx = []
            lds = []
            lrp = []
            for c in r.countries.all():
                try:
                    cc = XBRLCountryYearData.objects.get(country=c, year=project.year)
                    # print(cc, cc.tax_rate, cc.rating_based_default_spread, cc.country_risk_premium_rating)
                    if cc.tax_rate is not None:
                        ltx.append(float(cc.tax_rate))
                    if cc.rating_based_default_spread is not None:
                        lds.append(float(cc.rating_based_default_spread))
                    if cc.country_risk_premium_rating is not None:
                        lrp.append(float(cc.country_risk_premium_rating))
                except Exception as ex:
                    pass
                    # print(c, ex)
            try:
                tx, ds, rp = round(100 * sum(ltx) / len(ltx)) / 100, round(100 * sum(lds) / len(lds)) / 100, round(
                    100 * sum(lrp) / len(lrp)) / 100
                # print(tx, ds, rp)
                rr, c = XBRLRegionYearData.objects.get_or_create(region=r, year=project.year)
                rr.tax_rate = tx
                rr.country_risk_premium_rating = rp
                rr.rating_based_default_spread = ds
                rr.save()
            except Exception as ex:
                log_debug("update_region_risk_premium: " + str(ex))
        dic = {'status': 'ok'}
        log_debug("End update_region_risk_premium.")
        return dic

#   --- Stage 3 - SP500 ---
#     loading excel file to XBRLHistoricalReturnsSP.
    def load_sp_returns(self):
        log_debug("Start load_sp_returns.")
        # https://github.com/7astro7/full_fred
        file = 'histretSP'
        df = self.load_excel_data(file, 'Data')
        df = df.sort_values(by=['year'])
        spi = 1
        bbbi = 1
        n = 0
        XBRLHistoricalReturnsSP.truncate()
        log_debug("XBRLHistoricalReturnsSP.truncate() done.")
        # print(df)

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
                print('ex')
                print(ex)
                print('ex')
                log_debug('Error 1 create year_data: ' + str(r['year']) + " " + ex)

            try:
                year_data.save()
                if int(year_data.year) >= 1928:
                    spi = spi * (1 + year_data.return_on_sp500)
                    bbbi = bbbi * (1 + year_data.return_on_tbond)
                    n += 1
                    spi_ = spi ** (1 / n)
                    bbbi_ = bbbi ** (1 / n)
                    r = spi_ - bbbi_
                    year_data.risk_premium = round(10000 * r) / 10000
                year_data.save()
            except Exception as ex:
                log_debug('Error 2 year_data.save(): ' + str(r['year']) + " " + ex)
        dic = {'status': 'ok'}
        log_debug("End load_sp_returns.")
        return dic

    def get_etfs(self, params):
        # print(55555)
        # print(params)
        # print(55555)
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        driver = webdriver.Chrome()
        url = "https://www.cnbc.com/sector-etfs/"
        driver.get(url)

        headers = {'User-Agent': 'amos@drbaranes.com'}
        edgar_resp = requests.get(url, headers=headers, timeout=30)
        edgar_str = edgar_resp.text
        # print(edgar_str)

        # Find the document links
        soup = BeautifulSoup(edgar_str, 'html.parser')
        table_tag = soup.find('table', class_='BasicTable-table')
        print(table_tag)
        try:
            rows = table_tag.find_all('tr')
            print(rows)
        except Exception as ex:
            return dic_company_info

        # # Obtain HTML for document page
        # dic_data = {}
        # for row in rows:
        #     try:
        #         cells = row.find_all('td')
        #         if len(cells) > 3:
        #             if cells[0].text.lower() != type_.lower():
        #                 continue
        #             # for filing_year in range(2019, 2020):
        #             for filing_year in range(self.xbrl_start_year, self.today_year + 1):
        #                 if str(filing_year) in cells[3].text:
        #                     # print(str(filing_year), cells[3].text, cells[1].a['href'], cells[0].text)
        #                     if filing_year not in dic_data and (cells[0].text == "10-K" or cells[0].text == "20-F"):
        #                         dic_data[filing_year] = {}
        #                         dic_data[filing_year]['href'] = 'https://www.sec.gov' + cells[1].a['href']
        #     except Exception as ex:
        #         pass
        #
        # dic_company_info['data'] = dic_data
        # # print(dic_company_info)
        # return dic_company_info

        result = {}
        return result


class FinancialAnalysis(object):
    def __init__(self):
        try:
            clear_log_debug()
        except Exception as ex:
            pass

    def update_chart_of_accounts(self, **kwargs):
        log_debug('start: update_chart_of_accounts')
        for account in XBRLValuationAccounts.objects.all():
            # print('-' * 50)
            # print(account.id, account.order, account.statement.id, account.statement.statement, account.sic,
            #       account.account, account.type, account.scale)
            try:
                a, c = XBRLDimAccount.objects.get_or_create(order=account.order, account=account.account,
                                                        statement_order=account.statement.order,
                                                        statement=account.statement.statement)
            except Exception as ex:
                print('Error 5432: '+str(ex))
        log_debug('End: update_chart_of_accounts')
        result = {'status': "ok"}
        return result

    def update_companies(self, **kwargs):
        # print("update_companies")
        for company in XBRLCompanyInfo.objects.all():
            if company.is_active:
                # print('-'*10)
                # print(company.id, company.industry.main_sic.sic_code, company.industry.main_sic.sic_description,
                #       company.industry.sic_code, company.industry.sic_description,
                #       company.ticker, company.cik, company.company_name, company.exchange,
                #       company.is_active, company.city, company.state, company.zip)
                log_debug(company.ticker)
                # print(company.country_of_incorporation.name)
                # print(company)
                a, c = XBRLDimCompany.objects.get_or_create(id=company.id,
                                                            main_sic_code=company.industry.main_sic.sic_code,
                                                            main_sic_description=company.industry.main_sic.sic_description,
                                                            sic_code=company.industry.sic_code,
                                                            sic_description=company.industry.sic_description,
                                                            ticker=company.ticker, cik=company.cik,
                                                            company_name=company.company_name,
                                                            exchange=company.exchange,
                                                            city=company.city,
                                                            state=company.state,
                                                            zip=company.zip, is_active=company.is_active)
        result = {'status': "ok"}
        # print(result)
        return result

    def update_time(self, **kwargs):
        print("update_time")
        up_to_year = datetime.datetime.now().year + 2

        for y in range(2012, up_to_year):
            for q in range(0, 5):
                ind = y * 10 + q
                log_debug(str(ind) + " " + str(y) + " " + str(q))
                a, c = XBRLDimTime.objects.get_or_create(id=ind, year=y, quarter=q)
        result = {'status': "ok"}
        # print(result)
        return result

    # https://webix-ui.medium.com/top-7-javascript-pivot-widgets-in-2019-2020-8d81d4042f51
    # https://github.com/nicolaskruchten/pivottable
    def update_fact_table(self, **kwargs):
        log_debug("--update_chart_of_accounts--")
        ticker_ = kwargs['ticker'].upper()
        log_debug(ticker_)
        # print("--update_chart_of_accounts--")
        # request = kwargs['request']
        # print(ticker_)
        company = XBRLCompanyInfo.objects.get(ticker=ticker_)
        log_debug("got company: " + ticker_)
        try:
            company_ = XBRLDimCompany.objects.get(ticker=ticker_)
        except Exception as ex:
            log_debug("Error 9876: " + ticker_ + str(ex))

        log_debug("Start yearly data")
        for y in company.financial_data['data']:
            try:
                yd = company.financial_data['data'][y]
                if int(yd['dei']['documentfiscalyearfocus']) < 2012:
                    continue
                yq = int(yd['dei']['documentfiscalyearfocus'] + "0")
                time_ = XBRLDimTime.objects.get(id=yq)
                log_debug("start update fact table for " + ticker_ + " year: " + str(y))
                for account in yd['year_data']:
                    # print(account)
                    account_ = XBRLDimAccount.objects.get(order=int(account))
                    amount_ = yd['year_data'][account]
                    # print('account_')
                    # print(account_)
                    # print('amount_')
                    # print(amount_)
                    try:
                        f, c = XBRLFactCompany.objects.get_or_create(company=company_, time=time_, account=account_)
                        # print(f)
                        f.amount = amount_
                        f.save()
                        # print('--saved--')
                    except Exception as ex:
                        log_debug(str(ex))
                        # print(str(account_) + "  " + str(ex))
                log_debug("End update fact table for " + ticker_ + " year: " + str(y))
            except Exception as ex:
                log_debug("Err 9123: "+str(ex))
                continue

        log_debug("Start quarterly data")
        for y in company.financial_dataq['data']:
            try:
                for sq in company.financial_dataq['data'][y]:
                    yd = company.financial_dataq['data'][y][sq]
                    if int(yd['dei']['documentfiscalyearfocus']) < 2012:
                        continue
                    q = yd['dei']['documentfiscalperiodfocus'][1]
                    log_debug("start update fact table for ticker=" + ticker_ + " year=" + str(y) + " q=" + str(q))
                    yq = int(yd['dei']['documentfiscalyearfocus'] + str(q))
                    time_ = XBRLDimTime.objects.get(id=yq)
                    for account in yd['year_data']:
                        account_ = XBRLDimAccount.objects.get(order=int(account))
                        amount_ = yd['year_data'][account]
                        try:
                            f, c = XBRLFactCompany.objects.get_or_create(company=company_, time=time_, account=account_)
                            f.amount = amount_
                            f.save()
                        except Exception as ex:
                            log_debug(str(ex))
                    log_debug("End update fact table for ticker=" + ticker_ + " year=" + str(y) + " q=" + str(q))
            except Exception as ex:
                log_debug("Err 6537: "+str(ex))
                continue

        log_debug("End quarterly data")
        result = {'status': "ok"}
        # print(result)
        return result

    def get_data_for_ticker(self, **kwargs):
        print('get_data_for_ticker 1')
        ticker_ = kwargs['ticker'].upper()
        print('-' * 50)
        print(ticker_)
        qsv = XBRLFactCompany.objects.filter(company__ticker=ticker_, time__quarter__lte=0).all().values("company_id",
                                                                                                         "time_id",
                                                                                                         "account_id",
                                                                                                         "amount")

        # qsv = XBRLFactCompany.objects.filter(company__ticker=ticker_, time__quarter__gt=0).all().values("time_id", "account_id", "amount")
        print(qsv)

        df = pd.DataFrame(qsv)
        print(df)
        df = df.pivot(index='account_id', columns='time_id', values='amount')
        print(df)

        result = {'status': "ok"}
        # print(result)
        return result

    def get_pivot_data(self, dic):
        dic = eval(dic)
        # print('get_data_for_ticker 1')
        ticker_ = dic['ticker']
        # print(ticker_)
        sic_ = XBRLDimCompany.objects.get(ticker=ticker_).sic_code
        companies = XBRLDimCompany.objects.filter(sic_code=sic_).all()
        companies_dic = {}
        for c in companies:
            companies_dic[c.id] = c.company_name
        qsv = XBRLFactCompany.objects.filter(company__sic_code=sic_, time__quarter__lte=0).all().values("company_id", "time_id", "account_id", "amount")
        company_id = []
        time_id = []
        account_id = []
        amount = []
        for q in qsv:
            # print(q, q['time_id'], q['account_id'],q['amount'])
            company_id.append(q['company_id'])
            time_id.append(q['time_id'])
            account_id.append(q['account_id'])
            amount.append(float(q['amount']))

        data_ = {"company_id": company_id, "time_id": time_id, "account_id": account_id, "amount": amount, "companies_dic": companies_dic, "sic":sic_}
        # print(data_)
        result = {'status': "ok", "data": data_}

        # print(result)
        return result
