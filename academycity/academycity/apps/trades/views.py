from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
import time
import os
import pickle
import numpy as np
import scipy.stats as si
from django.conf import settings
from django.views.generic import ListView
from concurrent.futures import ProcessPoolExecutor as P
from multiprocessing import cpu_count
from random import randint
from django.views.generic import TemplateView
from .models import PlacedOrders

import asyncio
asyncio.set_event_loop(asyncio.get_event_loop_policy().new_event_loop())
from ib_insync import IB, util, Forex, Option


def home(request):
    # print('trades-home')
    title = _('Trades App')
    return render(request, 'trades/home.html', {'title': title})


def currency_exchange(request, currencies='EURUSD'):
    # print(currencies)
    ss1 = 'ss1'
    ss2 = 'ss2'
    ss3 = 'ss3'
    ss4 = 'ss4'
    ss5 = 'ss5'
    ss6 = 'ss6'
    ss7 = 'ss7'
    ss8 = 'ss8'
    ss9 = 'ss9'
    df = None
    is_error = 0
    try:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        ib_server = 'twoprojectsib1_tws_1'
        ib_port = 4003
        if settings.DEBUG:
            ib_server = '127.0.0.1'
            ib_port = 4002
        ib_ = IB()
        ci = randint(0, 100000)
        ib_.connect(ib_server, ib_port, clientId=ci)
        # print('ib_')
        # print(ib_)
        # print('ib_')
        ss1 = str(ib_)
    except Exception as e:
        ss1 = "Error connecting to: " + ib_server + ":" + str(ib_port)
        ss2 = e
        is_error = 1

    try:
        c = Forex(currencies)
        bars = ib_.reqHistoricalData(c, endDateTime='', durationStr='1 D',
                                     barSizeSetting='1 min', whatToShow='MIDPOINT', useRTH=True)
        # print(bars)
        ss3 = 'good 3'
        df = util.df(bars)
        # print(df[['date', 'open', 'high', 'low', 'close']])
        ss4 = 'good 4'
        df = df.sort_values(by=['date'], ascending=False)
        ss5 = 'good 5'

        ib_.disconnect()
        del ib_

        ss6 = 'good 6'
    except Exception as e2:
        ss7 = e2
        is_error = 1

    context = {
        'df': df,'ss1': ss1,'ss2': ss2,'ss3': ss3,'ss4': ss4,'ss5': ss5,'ss6': ss6,'ss7': ss7,'ss8': ss8,'ss9': ss9,
        'is_error' : is_error,
        'currencies': currencies,
        'title': 'Currency Exchange',
        'cur_list': ['GBPUSD','GBPZAR','HKDJPY','KRWAUD','KRWCAD','KRWCHF',
                     'KRWEUR','KRWGBP','KRWHKD','KRWJPY','KRWUSD','MXNJPY','NOKJPY','NOKSEK','NZDCAD','NZDCHF','NZDJPY',
                     'NZDUSD','SEKJPY','SGDCNH','SGDJPY','TRYJPY','USDCAD','USDCHF','USDCNH','USDCZK','USDDKK','USDHKD',
                     'USDHUF','USDILS','USDJPY','USDKRW','USDMXN','USDNOK','USDPLN','USDRUB','USDSEK','USDSGD','USDTRY',
                     'USDZAR','ZARJPY','EURPLN','EURRUB','EURSEK','EURSGD','EURTRY','EURUSD','EURZAR','GBPAUD','GBPCAD',
                     'GBPCHF','GBPCNH','GBPCZK','GBPDKK','GBPHKD','GBPHUF','GBPJPY','GBPMXN','GBPNOK','GBPNZD','GBPPLN',
                     'GBPSEK','GBPSGD','GBPTRY','GBPUSD','GBPZAR','HKDJPY','KRWAUD','KRWCAD','KRWCHF','KRWEUR','KRWGBP',
                     'KRWHKD','KRWJPY','KRWUSD','MXNJPY','NOKJPY','NOKSEK','NZDCAD','NZDCHF','NZDJPY','NZDUSD','SEKJPY',
                     'SGDCNH','SGDJPY','TRYJPY','USDCAD','USDCHF','USDCNH','USDCZK','USDDKK','USDHKD','USDHUF','USDILS',
                     'USDJPY','USDKRW','USDMXN','USDNOK','USDPLN','USDRUB','USDSEK','USDSGD','USDTRY','USDZAR','ZARJPY']
    }
    return render(request, 'trades/currency_exchange.html', context)


def option_trading(request):
    title = 'option_trading'
    return render(request, 'trades/option_trading.html', {'title': title})


# Trading ---
def get_option_chain(request):
    print('get_option_chain: ', time.perf_counter())
    ib_server = 'twoprojectsib1_tws_1'
    ib_port = 4003
    try:
        if settings.DEBUG:
            ib_server = '127.0.0.1'
            ib_port = 4002
    except Exception as e:
        print(e)

    file_path = settings.DATA_ROOT
    ci = randint(0, 100000)
    tickers = [
               ('TEVA', 'CBOE', ci, ib_server, ib_port, file_path),
               ('AAPL', 'CBOE', ci+1, ib_server, ib_port, file_path),
               ('AMZN', 'CBOE', 1, ib_server, ib_port, file_path),
               ]
    # , ('AAPL', 'CBOE', ci+1, ib_server, ib_port, file_path)
    # ('TEVA', 'CBOE', ci+2, ib_server, ib_port, file_path),
    # ('AMZN', 'CBOE', 1, ib_server, ib_port, file_path),

    # create_runners_option_chain(tickers)
    with P(max_workers=cpu_count()) as pool:
        results = pool.map(create_arbitrage_on_symbol_option_chain, tickers)
        for result in results:
            pass
    #

    context = {
        'results': '',
        'title': 'Global Simulation Running option chain',
        'h1': 'Welcome to Algo-Trading, preparing option chain',
        'tickers': tickers
    }
    return render(request, 'trades/option_chain.html', context)


def create_arbitrage_on_symbol_option_chain(args):
    # ('TEVA', 'CBOE', ci, ib_server, ib_port, file_path)
    time.sleep(1)
    print('------create_arbitrage_on_symbol_option_chain 1-----------')
    print(args[0])
    print('------create_arbitrage_on_symbol_option_chain 2-----------')
    A = ArbitrageOnSymbol(args)
    print('------create_arbitrage_on_symbol_option_chain 3-----------')
    A.fetch_possible_contracts()
    print('------create_arbitrage_on_symbol_option_chain 4-----------')
    A.convert_data()
    print('------create_arbitrage_on_symbol_option_chain 5-----------')


#
def run_options_engine(request):
    print('run_options_engine 1  - : ', time.perf_counter())
    ib_server = 'twoprojectsib1_tws_1'
    ib_port = 4003
    if settings.DEBUG:
        ib_server = '127.0.0.1'
        ib_port = 4002

    file_path = settings.DATA_ROOT
    ci = randint(0, 100000)
    tickers = [('AAPL', 'CBOE', ci, ib_server, ib_port, file_path)]  # , ('TEVA', 'CBOE', 2, ib_server, ib_port, file_path)

    create_runners(tickers)

    # refresh_data(['AAPL'])   # 'TSLA' # 'TEVA' # 'AAPL' # 'AMZN' #

    context = {
        'title': 'Global Simulation Running',
        'h1': 'Welcome to the Options Algo-Trading',
        'tickers': tickers
    }
    return render(request, 'trades/algo_trading.html', context)


def create_runners(tickers):
    print('create_runners 1')
    with P(max_workers=cpu_count()) as pool:
        results = pool.map(create_arbitrage_on_symbol, tickers)
        for result in results:
            print(result)


def create_arbitrage_on_symbol(args):
    time.sleep(1)
    print('create_arbitrage_on_symbol 1 - :', args[0])
    A = ArbitrageOnSymbol(args)
    A.run()
    #return 1


class ArbitrageOnSymbol():
    def __init__(self, args):
        super(ArbitrageOnSymbol, self).__init__()
        print('ArbitrageOnSymbol__init__: ', args[0], args[1], args[2])
        # time.sleep(1)
        self.symbol = args[0]
        self.exchange = args[1]
        self.clientId = args[2]
        self.ib_server = args[3]
        self.ib_port = args[4]
        self.file_path = args[5]
        #
        self.is_refresh_source = False
        self.is_refresh = False
        #
        self.Storage = self.file_path + '/Storage_' + self.symbol
        self.Storage_ = self.file_path + '/Storage__' + self.symbol
        #self.data = self.get_data()
        #
        self.start_time = time.perf_counter()
        self.amount_of_arbitrages = 0
        self.test_counter = 0
        #asyncio.set_event_loop(asyncio.new_event_loop())

        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        self.ib_ = IB()
        self.data = None
        print('End ArbitrageOnSymbol__init__: ', args[0], args[1], args[2])

    # pull data and store locally
    def fetch_possible_contract(self, right='C'):
        print('fetch_possible_contract------ 1')
        print(right, ' ', self.symbol)
        o = Option(symbol=self.symbol, right=right, exchange=self.exchange)
        # print('fetch_possible_contract 1: ', self.symbol, ' ', right)
        o_cd = self.ib_.reqContractDetails(o)
        # print('fetch_possible_contract 2: ', self.symbol, ' ', right)
        cs = [j.contract for j in o_cd]
        print('fetch_possible_contract------ 2')
        print('Done: ', right, ' ', self.symbol)
        print('fetch_possible_contract------ 3')
        return cs

    def fetch_possible_contracts(self):
        # loop = asyncio.get_event_loop()

        #loop = asyncio.get_event_loop_policy().new_event_loop()
        #asyncio.set_event_loop(loop)

        try:
            print('fetch_possible_contracts 1')
            self.ib_.connect(self.ib_server, self.ib_port, clientId=self.clientId)
            print('fetch_possible_contracts 2')
            print(self.ib_)
            #####
            print('fetch_possible_contracts 3')
            c = self.fetch_possible_contract('C')
            p = self.fetch_possible_contract('P')
            print('fetch_possible_contracts 4')

            possible_contracts = {'C': c, 'P': p}
            if os.path.exists(self.Storage):
                os.remove(self.Storage)
            with open(self.Storage, 'wb') as f:
                pickle.dump(possible_contracts, f)
            print('fetch_possible_contracts 5')

            return possible_contracts
            #####
        except KeyboardInterrupt:
            pass
        finally:
            print("ib_.disconnect")
            # self.ib_.disconnect()
            print("Closing Loop")
            #loop.close()

    # fetching the data
    def get_possible_contracts(self):
        print('get_possible_contracts 1')
        with open(self.Storage, 'rb') as f:
            return pickle.load(f)

    def convert_data(self):
        if os.path.exists(self.Storage_):
            os.remove(self.Storage_)
        data = {}
        data_ = self.get_possible_contracts()  # for every right (C or P) we have list of contract
        print('convert_data - 1')
        data['C'] = self.get_data_('C', data_['C'])
        data['P'] = self.get_data_('P', data_['P'])
        with open(self.Storage_, 'wb') as f:
            pickle.dump(data, f)
        print('convert_data - 2')
        return data

    # Create three dictionaries
    # cs = strikes for each contract period
    # cc_c = contracts for each contract period
    # bf = possible butterfly
    def get_data_(self, right, data):
        print('---------------------')
        print('-----get_data_--------', right)
        print('---------------------')
        cs = {}  # strikes for each contract period
        cs0 = {}  # strikes for each contract period
        for i in data:
            h = i.lastTradeDateOrContractMonth
            if h not in cs:
                cs[h] = {'strikes': {str(i.strike): {'event': None, 'bid': 0, 'bidSize': 0, 'ask': 0, 'askSize': 0,
                                                     'close': 0, 'price': 0, 'undPrice': 0, 'contract': i}}, 'strategies': []}
                cs0[h] = [i.strike]
            else:
                cs[h]['strikes'][str(i.strike)] = {'event': None, 'bid': 0, 'bidSize': 0, 'ask': 0, 'askSize': 0,
                                                   'close': 0, 'price': 0, 'undPrice': 0, 'contract': i}
                cs0[h].append(i.strike)
        for h in cs0:
            cs0[h] = sorted(cs0[h])
            oo = cs0[h]
            pp = []
            for v in range(1, len(oo)):
                pp.append(float(oo[v]) - float(oo[v - 1]))
            dd1 = []
            for pi in pp:
                if pi not in dd1:
                    dd1.append(pi)
            dd1 = sorted(dd1)
            df = int(max(oo) / min(dd1))
            dd = []
            for d1 in dd1:
                for f in range(1, df):
                    dk = d1 * f
                    if dk not in dd:
                        dd.append(dk)
            for d in dd:
                for v in range(1, len(oo)):
                    if ((oo[v] + d) in oo) and ((oo[v] - d) in oo):
                        k = ((oo[v] - d), oo[v], (oo[v] + d))
                        cs[h]['strategies'].append(k)
        print('End ---------------------')
        print('-----get_data_--------', right)
        print('End ---------------------')
        return cs
    # end fetching the data

    # run the algo trading
    def run(self):
        print("run 1: Process for {}".format(self.symbol))
        self.data = self.get_data()
        print("run 2: Process for {}".format(self.symbol))
        #loop = asyncio.get_event_loop()

        #loop = asyncio.get_event_loop_policy().new_event_loop()
        #asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        print(loop)
        print("run 3: Process for {}".format(self.symbol))
        while True:
            print("run 1 While Loop", ' ', self.symbol)
            try:
                print("run 2 While Loop", ' ', self.symbol)
                self.ib_.connect(self.ib_server, self.ib_port, clientId=self.clientId)
                print("run 3 While Loop", ' ', self.symbol)
                print(self.ib_)

                #####
                # kk = '20190802'
                # self.objects_.append(ArbitrageOnContract('C', kk, self.data['C'][kk], loop, self))
                #####
                loop.create_task(self.main())
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            finally:
                print("finally Closing Loop", ' ', self.symbol)
                self.ib_.disconnect()
        loop.close()

    async def main(self):
        print('main 1 ', self.symbol)
        for contracts_right in self.data:
            # print('main ', contracts_right)
            for contract_date in self.data[contracts_right]:
                await asyncio.sleep(0)
                contracts_data = self.data[contracts_right][contract_date]
                print(contract_date)
                s = asyncio.ensure_future(self.running(contracts_right, contract_date, contracts_data, self.exchange))

    def get_data(self):
        with open(self.Storage_, 'rb') as f:
            return pickle.load(f)

    async def running(self, contracts_right, contract_date, contracts_data, exchange):
        # print(self.symbol, ': ', contracts_right, ' - running - ', contract_date, '\n',contracts_data,'\n',exchange)
        # await asyncio.sleep(1)
        start_inner_time = time.perf_counter()
        price_tasks = []
        for s in contracts_data['strikes']:
            contracts_data['strikes'][s]['event'] = asyncio.Event()
            contracts_data['strikes'][s]['price'] = 0
            c = contracts_data['strikes'][s]['contract']
            o_price_fut = asyncio.ensure_future(self.ib_.reqTickersAsync(c))
            price_task = asyncio.ensure_future(self.add_success_callback(o_price_fut,
                                                                         self.put_price_in_array, contracts_data))
            price_tasks.append(price_task)
        self.get_legs_arrived_tasks(contracts_right, contract_date, contracts_data, exchange)
        results = await asyncio.gather(*price_tasks)

        end_time = time.perf_counter()
        #print('End of running ', contracts_right, ' ', contract_date, ' Time of running: ',
        #      end_time-start_inner_time, ' ', ' Total time:', end_time-self.start_time, 'Prices:\n', results)
        await self.running(contracts_right, contract_date, contracts_data, exchange)

    async def add_success_callback(self, fut, callback, *args, **kwargs):
        result = await fut
        result = callback(result, *args, **kwargs)
        return result

    async def get_legs_arrived_task(self, strategy, contracts_right, contract_date, contracts_data, exchange):
        await contracts_data['strikes'][str(strategy[0])]['event'].wait()
        await contracts_data['strikes'][str(strategy[1])]['event'].wait()
        await contracts_data['strikes'][str(strategy[2])]['event'].wait()
        await self.calculate_butterfly(strategy, contracts_right, contract_date, contracts_data, exchange)
        return strategy

    def get_legs_arrived_tasks(self, contracts_right, contract_date, contracts_data, exchange):
        legs_arrived_tasks = []
        # print(contracts_data)
        # await asyncio.sleep(1)
        for strategy in contracts_data['strategies']:
            task = asyncio.ensure_future(self.get_legs_arrived_task(strategy, contracts_right, contract_date,
                                                                    contracts_data, exchange))
            legs_arrived_tasks.append(task)
        return legs_arrived_tasks

    # From here need to fix
    def put_price_in_array(self, ticker, contracts_data):
        try:
            t = ticker[0]
            #print('t0----')
            #print(t)
            #print('--0000---')
            #print(t.bidGreeks)
            #print('---11111---')
            #print(t.bidGreeks.undPrice)
            #print('t2222----')

            p = (t.ask + t.bid) / 2

            contracts_data['strikes'][str(t.contract.strike)]['bid'] = t.bid
            contracts_data['strikes'][str(t.contract.strike)]['bidSize'] = t.bidSize
            contracts_data['strikes'][str(t.contract.strike)]['ask'] = t.ask
            contracts_data['strikes'][str(t.contract.strike)]['askSize'] = t.askSize
            contracts_data['strikes'][str(t.contract.strike)]['close'] = t.close

            contracts_data['strikes'][str(t.contract.strike)]['price'] = p
            # print(contracts_data['strikes'][str(t.contract.strike)])

            contracts_data['strikes'][str(t.contract.strike)]['undPrice'] = t.bidGreeks.undPrice

            contracts_data['strikes'][str(t.contract.strike)]['event'].set()
            return p
        except Exception as e:
            print('=======ERRORR==============="')
            print(e)
            print('=======End ERRORR==============="')


    # need to improve.
    async def calculate_butterfly(self, strategy, contracts_right, contract_date, contracts_data, exchange):
        l = contracts_data['strikes'][str(strategy[0])]['ask']
        m = contracts_data['strikes'][str(strategy[1])]['bid']
        r = contracts_data['strikes'][str(strategy[2])]['ask']
        u0 = contracts_data['strikes'][str(strategy[0])]['undPrice']
        u1 = contracts_data['strikes'][str(strategy[1])]['undPrice']
        u2 = contracts_data['strikes'][str(strategy[2])]['undPrice']

        # print('u0: ', u0, 'u1: ', u1,'u2: ', u2)

        strategy_price = 999
        if l >-1 and m > -1 and r > -1:
            strategy_price = (l + r) - (2 * m)
            #if strategy_price < 100:
            #    await self.place_arbitrage(strategy, strategy_price, contracts_data, exchange)
            #    self.amount_of_arbitrages += 1
            if strategy_price < 0.09:
                await self.log_to_db(strategy, contracts_right, contract_date, contracts_data, strategy_price)
        return strategy_price

    # need to fix
    async def place_arbitrage(self, strategy, strategy_price, contracts_data, exchange):
        for s in contracts_data['strikes']:
            c = contracts_data['strikes'][s]['contract']
            if c.strike == strategy[0]:
                lc = c
            elif c.strike == strategy[1]:
                mc = c
            elif c.strike == strategy[2]:
                rc = c

        # x = [lc, mc, rc]
        # x1 = self.ib_.qualifyContracts(x)

        #self.ib_.qualifyContracts(mc)
        #self.ib_.qualifyContracts(rc)

        combo_legs = [
            ComboLeg(conId=lc.conId, ratio=1, action='BUY', exchange=exchange),
            ComboLeg(conId=mc.conId, ratio=2, action='SELL', exchange=exchange),
            ComboLeg(conId=rc.conId, ratio=1, action='BUY', exchange=exchange),
        ]

        c = Contract(symbol=self.parent.symbol, secType='BAG', exchange=exchange,
                     currency='USD', comboLegs=combo_legs)

        o = MarketOrder(action='BUY', totalQuantity=1000)

        # lo = LimitOrder(action='BUY', totalQuantity=1, lmtPrice=strategy_price)

        if self.test_counter < 3:
            # t = self.ib_.placeOrder(contract=c, order=o)
            print('------100')
            print('place_arbitrage: order issued ', strategy, strategy_price)
            print(c)
            print('------100')

            # print(t)
            self.test_counter += 1

    async def log_to_db(self, strategy, contracts_right, contract_date, contracts_data, strategy_price):
        # print('log_to_db: ', contracts_right, contract_date, ' ', strategy, ' ', strategy_price)
        lstrike = round(float(strategy[0]), 2)
        lb = round(contracts_data['strikes'][str(strategy[0])]['bid'],2)
        lbs = contracts_data['strikes'][str(strategy[0])]['bidSize']
        la = round(contracts_data['strikes'][str(strategy[0])]['ask'],2)
        las = contracts_data['strikes'][str(strategy[0])]['askSize']
        lc = round(contracts_data['strikes'][str(strategy[0])]['close'],2)
        lp = round(contracts_data['strikes'][str(strategy[0])]['price'],2)
        lu = round(contracts_data['strikes'][str(strategy[0])]['undPrice'],2)

        rstrike = float(strategy[2])
        rb = round(contracts_data['strikes'][str(strategy[2])]['bid'],2)
        rbs = contracts_data['strikes'][str(strategy[2])]['bidSize']
        ra = round(contracts_data['strikes'][str(strategy[2])]['ask'],2)
        ras = contracts_data['strikes'][str(strategy[2])]['askSize']
        rc = round(contracts_data['strikes'][str(strategy[2])]['close'],2)
        rp = round(contracts_data['strikes'][str(strategy[2])]['price'],2)
        ru = round(contracts_data['strikes'][str(strategy[2])]['undPrice'],2)

        mstrike =float(strategy[1])
        mb = round(contracts_data['strikes'][str(strategy[1])]['bid'],2)
        mbs = contracts_data['strikes'][str(strategy[1])]['bidSize']
        ma = round(contracts_data['strikes'][str(strategy[1])]['ask'],2)
        mas = contracts_data['strikes'][str(strategy[1])]['askSize']
        mc = round(contracts_data['strikes'][str(strategy[1])]['close'],2)
        mp = round(contracts_data['strikes'][str(strategy[1])]['price'],2)
        mu = round(contracts_data['strikes'][str(strategy[1])]['undPrice'],2)

        #print('==========================================')
        #print('lb: ', lb, ' lbs: ', lbs, ' la: ', la, ' las: ', las, ' lc: ', lc , ' lp: ',  lp , ' lu: ', lu)
        #print('rb: ', rb, ' rbs: ', rbs, ' ra: ', ra, ' ras: ', ras, ' rc: ', rc , ' rp: ',  rp , ' ru: ', ru)
        #print('mb: ', mb, ' mbs: ', mbs, ' ma: ', ma, ' mas: ', mas, ' mc: ', mc , ' mp: ',  mp , ' mu: ', mu)
        #print('-----------------+++++++++++++++++++++++++++++----------------------------------')

        try:
            PlacedOrders.objects.create(Right=contracts_right,
                                        Ticker=self.symbol,
                                        ContractDate=contract_date, LeftStrike=lstrike,
                                        LeftOrderAskPrice=la,
                                        LeftOrderBidPrice=lb,
                                        LeftOrderAveragePrice=lp,
                                        LeftOrderClose=lc,
                                        LeftOrderBidSize=lbs,
                                        LeftOrderAskSize=las,
                                        LeftActualPrice=0,
                                        LeftActualUndPrice=lu,
                                        MidStrike=mstrike,
                                        MidOrderAskPrice=ma,
                                        MidOrderBidPrice=mb,
                                        MidOrderAveragePrice=mp,
                                        MidOrderClose=mc,
                                        MidOrderBidSize=mbs,
                                        MidOrderAskSize=mas,
                                        MidActualPrice=0,
                                        MidActualUndPrice=mu,
                                        RightStrike=rstrike,
                                        RightOrderAskPrice=ra,
                                        RightOrderBidPrice=rb,
                                        RightOrderAveragePrice=rp,
                                        RightOrderClose=rc,
                                        RightOrderBidSize=rbs,
                                        RightOrderAskSize=ras,
                                        RightActualPrice=0,
                                        RightActualUndPrice=ru,
                                        StrategyPrice=strategy_price
                                        )
        except Exception as e:
            print("======ERROR-DB---------")
            print(e)
            print("======End ERROR-DB---------")


class OrdersView(ListView):
    template_name = 'trades/orders_list.html'
    model = PlacedOrders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = PlacedOrders.objects.order_by('-OrderDate')[:20]

        context['orders'] = orders

        return context
