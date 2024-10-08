from ...ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
import matplotlib as mpl
mpl.use('Agg')


from datetime import datetime, timedelta

"""
 to_data_path_ is the place datasets are kept
 topic_id name of the chapter to store images
"""

import pandas as pd
from django.apps import apps
# ---
from abc import ABC, abstractmethod
# ----
import warnings
warnings.filterwarnings('ignore')



class TickData(object):
    # Stores a single unit of data
    def __init__(self, timestamp='', open_price=0, high_price=0, low_price=0, close_price=0, total_volume=0):
        self.timestamp = timestamp
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.total_volume = total_volume
    def get_list(self):
        return [self.timestamp, self.open_price, self.close_price,self.high_price, self.low_price, self.total_volume]

class Order(object):
    def __init__(self, timestamp, qty, is_buy, is_market_order, price=0):
        self.timestamp = timestamp
        self.qty = qty
        self.price = price
        self.is_buy = is_buy
        self.is_market_order = is_market_order
        self.is_filled = False
        self.filled_price = 0
        self.filled_time = None
        self.filled_qty = 0

class Position(object):
    def __init__(self, strategy=None):
        self.buys = self.sells = self.net = 0
        self.rpnl = [0]
        self.position_value = 0
        self.log_position_status = pd.DataFrame()
        self.strategy = strategy
        self.is_long = self.is_short = False

    def on_order_filled_event(self, is_buy, qty, price):
        if is_buy:
            self.buys += qty
        else:
            self.sells += qty

        self.net = self.buys - self.sells

        self.is_long = self.net > 0
        self.is_short = self.net < 0

        changed_value = qty * price * (-1 if is_buy else 1)
        self.position_value += changed_value

        if self.net == 0:
            self.rpnl.append(self.position_value)
            self.position_value = 0
            self.strategy.last_sell_price = [0]
            self.strategy.last_buy_price = [0]

    def calculate_unrealized_pnl(self, price):
        if self.net == 0:
            return 0
        market_value = self.net * price
        upnl = self.position_value + market_value
        return upnl

    def log_data(self, timestamp, field, value):
        # print("log_data", timestamp, field, value)
        self.log_position_status.loc[timestamp, field] = value

    def update_position_status(self):
        timestamp = self.strategy.recent_data_ticker.timestamp
        close_price = self.strategy.recent_data_ticker.close_price
        upnl = self.calculate_unrealized_pnl(close_price)
        # print(timestamp.date(), 'POSITION', 'value:%.3f' % self.position_value, 'upnl:%.3f' % upnl, 'rpnl:%.3f' % self.rpnl)
        self.log_data(timestamp, 'position_value', round(100*self.position_value)/100)
        self.log_data(timestamp, 'upnl', round(100*upnl)/100)
        self.log_data(timestamp, 'rpnl', round(100*sum(self.rpnl))/100)
        self.log_data(timestamp, 'net', self.net)
        self.log_data(timestamp, 'is_short', self.is_short)
        self.log_data(timestamp, 'is_long', self.is_long)

    def get_chart_data(self, l, scale=1):
        re = {'timestamp': []}
        for c in l:
            re[c] = []
        for timestamp, row in self.log_position_status.iterrows():
            is_continue = False
            for c in l:
                if str(row[c]) == 'nan':
                    is_continue = True
            if is_continue:
                # print(timestamp)
                continue
            for c in l:
                re[c].append(round(scale*10000*row[c])/10000)
            t = str(timestamp).split(' ')[0]
            re['timestamp'].append(t)
            # print("added data",timestamp)
        # print(l, "\n\n", min(re['timestamp']), max(re['timestamp']), "\n\n")
        # print(l, "\n\n", len(re['timestamp']), len(re[l[0]]), "\n\n")
        return re

class Strategy:
    def __init__(self, **kwargs):
        self.engin = None
        self.unfilled_orders = []
        self.position = Position(strategy=self)
        self.timestamp = None
        self.recent_data_ticker = None

    # --- update_tick_event ---
    def update_tick_event(self):
        self.set_data()
        self.generate_signals_and_send_order()

    @abstractmethod
    def set_data(self):
        print("Over load this function 22-22-1")

    @abstractmethod
    def generate_signals_and_send_order(self):
        print("Over load this function 22-22-2")

    # --- match_order_book ---
    def match_order_book(self):
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = [
                order for order in self.unfilled_orders
                if self.match_unfilled_orders(order)
            ]

    @abstractmethod
    def match_unfilled_orders(self, order):
        print("Over load this function 22-22-3")

    # ===================
    def on_tick_event(self, timestamp):
        # print("on_tick_event: ", timestamp)
        self.timestamp = timestamp
        row = self.engin.df.loc[timestamp]
        # print(row)
        open_price = float(row['Open'])
        high_price = float(row['High'])
        low_price = float(row['Low'])
        close_price = float(row['Close'])
        volume = int(row['Volume'])
        # print(timestamp.date(), 'TICK', self.symbol, 'open:', open_price, 'close:', close_price)
        self.recent_data_ticker = TickData(timestamp, open_price, high_price, low_price, close_price, volume)
        # print("self.recent_data_ticker\n", self.recent_data_ticker.get_list())
        # -------------------------------------------
        self.update_tick_event()
        # ---
        self.match_order_book()
        # ---
        self.position.update_position_status()


class MeanRevertingStrategy(Strategy):
    def __init__(self, engin, lookback_intervals = 0, buy_threshold = 1.0, sell_threshold = 1.0, **kwargs):
        super(MeanRevertingStrategy, self).__init__(**kwargs)
        self.prices = pd.DataFrame()
        self.engin = engin
        self.trade_qty = engin.trade_qty
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    # --- match_order_book ---
    def match_unfilled_orders(self, order):
        timestamp = self.timestamp
        """ Order is matched and filled """
        if order.is_market_order and timestamp >= order.timestamp:
            close_price = self.recent_data_ticker.close_price

            order.is_filled = True
            order.filled_timestamp = timestamp
            order.filled_price = close_price
            self.on_order_filled(order.qty, order.is_buy, close_price, timestamp)
            return False

        return True

    def on_order_filled(self, qty, is_buy, filled_price, timestamp):
        self.position.on_order_filled_event(is_buy, qty, filled_price)

    # -----------------------------------------------
    def set_data(self):
        timestamp = self.timestamp
        self.prices = self.engin.df.loc[:timestamp]

    def generate_signals_and_send_order(self):
        if self.prices.shape[0] < self.lookback_intervals:
            return
        timestamp = self.timestamp
        signal_value = self.calculate_z_score()

        if self.buy_threshold > signal_value and not self.position.is_long:
            # print(timestamp.date(), "BUY signal self.buy_threshold", self.buy_threshold, "signal_value", signal_value)
            self.send_market_order(self.trade_qty, True, timestamp)
        elif self.sell_threshold < signal_value and not self.position.is_short:
            # print(timestamp.date(), "SELL signal self.sell_threshold" , self.sell_threshold , "signal_value", signal_value)
            self.send_market_order(self.trade_qty, False, timestamp)

    def send_market_order(self, qty, is_buy, timestamp):
        """ Adds an order to the order book """
        order = Order(timestamp, qty, is_buy, is_market_order=True, price=0, )
        # print(order.timestamp.date(), 'ORDER', 'BUY' if order.is_buy else 'SELL', order.qty)
        self.unfilled_orders.append(order)

    def calculate_z_score(self):
        # print("AA self.prices\n", self.prices, "\n", self.prices.shape)
        prices_ = self.prices[-self.lookback_intervals:]
        returns = prices_['Close'].pct_change().dropna()

        returns_ = returns[:-1]
        last_return = float(returns.iloc[-1])

        # print("DDDDDDDdd\n", returns, "\nDDDDDDDdd\n", returns_)
        # print(last_return)

        z_score = ((last_return - returns_.mean()) / returns_.std())
        # print("z_score", z_score)
        return z_score
    # -----------------------------------------------


# ------- Multiple Positions fulfill position based on list of previous prices----------
class MeanRevertingStrategyMP(Strategy):
    def __init__(self, engin, lookback_intervals = 0, buy_threshold = 1.0, sell_threshold = 1.0, **kwargs):
        super(MeanRevertingStrategyMP, self).__init__(**kwargs)
        self.prices = pd.DataFrame()
        self.engin = engin
        self.trade_qty = engin.trade_qty
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        # ---
        self.last_high_price = self.last_low_price = 0
        self.last_sell_price = self.last_buy_price = [0]
        # ---

    # --- match_order_book ---
    def match_unfilled_orders(self, order):
        timestamp = self.timestamp
        """ Order is matched and filled """
        if order.is_market_order and timestamp >= order.timestamp:
            close_price = self.recent_data_ticker.close_price

            order.is_filled = True
            order.filled_timestamp = timestamp
            order.filled_price = close_price
            self.on_order_filled(order.qty, order.is_buy, close_price, timestamp)
            return False

        return True

    def on_order_filled(self, qty, is_buy, filled_price, timestamp):
        self.position.on_order_filled_event(is_buy, qty, filled_price)
        if is_buy:
            self.last_buy_price.append(filled_price)
            if self.last_low_price > filled_price:
                self.last_low_price = filled_price
        else:
            self.last_sell_price.append(filled_price)
            if self.last_high_price < filled_price:
                self.last_high_price = filled_price
        if self.position.is_short:
            self.last_buy_price = [0]
        if self.position.is_long:
            self.last_sell_price = [0]

    # -----------------------------------------------
    def set_data(self):
        timestamp = self.timestamp
        self.prices = self.engin.df.loc[:timestamp]

    def generate_signals_and_send_order(self):
        if self.prices.shape[0] < self.lookback_intervals:
            return
        timestamp = self.timestamp
        signal_value = self.calculate_z_score()
        if self.buy_threshold > signal_value:
            if self.position.is_short:
                if self.recent_data_ticker.close_price <= max(self.last_sell_price):
                    self.last_sell_price.remove(max(self.last_sell_price))
                    self.send_market_order(self.trade_qty, True, timestamp)
            else:
                self.send_market_order(self.trade_qty, True, timestamp)
        elif self.sell_threshold < signal_value:
            if self.position.is_long:
                if self.recent_data_ticker.close_price >= min(self.last_buy_price):
                    self.last_buy_price.remove(min(self.last_buy_price))
                    self.send_market_order(self.trade_qty, False, timestamp)
            else:
                self.send_market_order(self.trade_qty, False, timestamp)

    def send_market_order(self, qty, is_buy, timestamp):
        """ Adds an order to the order book """
        order = Order(timestamp, qty, is_buy, is_market_order=True, price=0, )
        # print(order.timestamp.date(), 'ORDER', 'BUY' if order.is_buy else 'SELL', order.qty)
        self.unfilled_orders.append(order)

    def calculate_z_score(self):
        prices_ = self.prices[-self.lookback_intervals:]
        returns = prices_['Close'].pct_change().dropna()

        returns_ = returns[:-1]
        last_return = float(returns.iloc[-1])

        # print("DDDDDDDdd\n", returns, "\nDDDDDDDdd\n", returns_)
        # print(last_return)

        z_score = ((last_return - returns_.mean()) / returns_.std())
        # print("z_score", z_score)
        return z_score
    # -----------------------------------------------


class MRSThreeLastPrices(Strategy):
    def __init__(self, engin, lookback_intervals = 20, lookback_short_intervals = 1, buy_threshold = 1.0, sell_threshold = 1.0, **kwargs):
        super(MRSThreeLastPrices, self).__init__(**kwargs)
        self.prices = pd.DataFrame()
        self.engin = engin
        self.trade_qty = engin.trade_qty
        self.lookback_intervals = lookback_intervals
        self.lookback_short_intervals = lookback_short_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        # ---
        self.last_high_price = self.last_low_price = 0
        self.last_sell_price = self.last_buy_price = [0]
        # ---
        # print("="*100, "\nMRSThreeLastPrices symbol=", engin.symbol, "\n", "="*100)
        # ---

    # --- match_order_book ---
    def match_unfilled_orders(self, order):
        timestamp = self.timestamp
        """ Order is matched and filled """
        if order.is_market_order and timestamp >= order.timestamp:
            #
            # Hear need to add code to send the order to the broker.
            #
            close_price = self.recent_data_ticker.close_price
            order.is_filled = True
            order.filled_timestamp = timestamp
            order.filled_price = close_price
            self.on_order_filled(order.qty, order.is_buy, close_price, timestamp)
            return False

        return True

    def on_order_filled(self, qty, is_buy, filled_price, timestamp):
        self.position.on_order_filled_event(is_buy, qty, filled_price)
        if is_buy:
            self.last_buy_price.append(filled_price)
            if self.last_low_price > filled_price:
                self.last_low_price = filled_price
        else:
            self.last_sell_price.append(filled_price)
            if self.last_high_price < filled_price:
                self.last_high_price = filled_price
        if self.position.is_short:
            self.last_buy_price = [0]
        if self.position.is_long:
            self.last_sell_price = [0]

    # -----------------------------------------------
    def set_data(self):
        timestamp = self.timestamp
        self.prices = self.engin.df.loc[:timestamp]

    def generate_signals_and_send_order(self):
        if self.prices.shape[0] < self.lookback_intervals:
            return
        timestamp = self.timestamp
        signal_value = self.calculate_z_score()

        if self.buy_threshold > signal_value:
            # if self.position.is_short:
            #     if self.recent_data_ticker.close_price <= max(self.last_sell_price):
            #         self.last_sell_price.remove(max(self.last_sell_price))
            #         self.send_market_order(self.trade_qty, True, timestamp)
            # else:
            #     self.send_market_order(self.trade_qty, True, timestamp)
            self.send_market_order(self.trade_qty, True, timestamp)
        elif self.sell_threshold < signal_value:
            # if self.position.is_long:
            #     if self.recent_data_ticker.close_price >= min(self.last_buy_price):
            #         self.last_buy_price.remove(min(self.last_buy_price))
            #         self.send_market_order(self.trade_qty, False, timestamp)
            # else:
            #     self.send_market_order(self.trade_qty, False, timestamp)
            self.send_market_order(self.trade_qty, False, timestamp)
        elif abs(signal_value) < 0.1:
            if self.position.is_short:
                self.send_market_order(-self.position.net, True, timestamp)
            else:
                self.send_market_order(self.position.net, False, timestamp)

    def send_market_order(self, qty, is_buy, timestamp):
        """ Adds an order to the order book """
        order = Order(timestamp, qty, is_buy, is_market_order=True, price=0, )
        # print(order.timestamp.date(), 'ORDER', 'BUY' if order.is_buy else 'SELL', order.qty)
        self.unfilled_orders.append(order)

    def calculate_z_score(self):
        # print("AA self.prices\n", self.prices, "\n", self.prices.shape)

        prices_ = self.prices['Close']
        lps = prices_[-self.lookback_intervals:-self.lookback_short_intervals].astype(float)
        sps = prices_.iloc[-self.lookback_short_intervals:]
        # print("lps\\n", lps.shape, "sps\\n", sps.shape)

        lpsm = lps.mean()
        spsm = sps.mean()
        # print(lpsm, spsm)
        lps_std = lps.std()
        z_score = (spsm - lpsm) / lpsm  # lps_std
        self.position.log_data(self.timestamp, 'spsm', round(100*spsm)/100)
        self.position.log_data(self.timestamp, 'lpsm', round(100*lpsm)/100)
        self.position.log_data(self.timestamp, 'lps_std', round(1000*lps_std)/1000)
        self.position.log_data(self.timestamp, 'close_price', self.recent_data_ticker.close_price)
        self.position.log_data(self.timestamp, 'z_score', round(1000*z_score)/1000)

        # returns = prices_['Close'].pct_change().dropna().astype(float)
        # returns_ = returns[:-self.lookback_short_intervals]
        # last_returns = returns.iloc[-self.lookback_short_intervals:]
        # # print(returns.shape,returns_.shape,last_returns.shape)
        # # print("DDDDDDDdd\n", returns, "\nDDDDDDDdd\n", returns_)
        # # print(last_return)
        # returns_mean = returns_.mean()
        # last_returns_mean = last_returns.mean()
        # returns_std = returns_.std()

        # self.position.log_data(self.timestamp, 'last_returns_mean', round(1000*last_returns_mean)/1000)
        # self.position.log_data(self.timestamp, 'returns_mean', round(1000*returns_mean)/1000)
        # self.position.log_data(self.timestamp, 'returns_std', round(1000*returns_std)/1000)
        # self.position.log_data(self.timestamp, 'close_price', self.recent_data_ticker.close_price)
        # z_score = ((last_returns_mean - returns_mean) / returns_.std())
        # self.position.log_data(self.timestamp, 'z_score', round(1000*z_score)/1000)

        # print("z_score", z_score)

        return z_score
    # -----------------------------------------------


class BacktestEngine:
    def __init__(self, symbol, trade_qty, start=None, end=None, df=None):
        self.symbol = symbol
        self.trade_qty = trade_qty
        self.start_date = start
        self.end_date = end
        self.df = df
        self.recent_tick_data = None
        # ---
        self.strategies = dict()
        # ---
        # print("="*100, "\nBacktestEngine symbol=", symbol, "\n", "="*100)
        # ---

    def start(self, dic):
        print('Backtest started...')
        # self.strategy = MeanRevertingStrategy(engin=self, **kwargs)
        try:
            thh = float(dic['thh'])
            thl = float(dic['thl'])
            lookback_intervals_ = int(dic['l_inter'])
            lookback_short_intervals_ = int(dic['s_inter'])
            buy_threshold_ = -thl
            sell_threshold_ = thh

            # self.strategies["MeanReverting"] = MeanRevertingStrategy(engin=self,
            #                                                                      lookback_intervals = lookback_intervals_,
            #                                                                      buy_threshold = buy_threshold_,
            #                                                                      sell_threshold=sell_threshold_
            #                                                                      )
            #
            # self.strategies["MeanRevertingStrategyMP"] = MeanRevertingStrategyMP(engin=self,
            #                                                                                  lookback_intervals = lookback_intervals_,
            #                                                                                  buy_threshold = buy_threshold_,
            #                                                                                  sell_threshold=sell_threshold_
            #                                                                      )

            self.strategies["MRSThreeLastPrices"] = MRSThreeLastPrices(engin=self,
                                                                       lookback_intervals=lookback_intervals_,
                                                                       lookback_short_intervals=lookback_short_intervals_,
                                                                       buy_threshold = buy_threshold_,
                                                                       sell_threshold=sell_threshold_)
        except Exception as ex:
            print("Error 55", ex)
        # print(self.df)

        for timestamp, row in self.df.iterrows():
            for strategy_name in self.strategies:
                self.strategies[strategy_name].on_tick_event(timestamp)

        dic = {}
        for strategy_name in self.strategies:

            print("\n", "="*50, "\nStrategy: ", strategy_name, "\n", "="*50)
            # print("log_position_status\n", self.strategies[strategy_name].position.log_position_status)
            # for timestamp, row in self.strategies[strategy_name].position.log_position_status.iterrows():
            #     print(timestamp,
            #           "value", str(round(100 * float(row["value"])) / 100),
            #           "urpnl", str(round(100 * float(row["upnl"])) / 100),
            #           "rpnl", str(round(100 * float(row["rpnl"])) / 100),
            #           "net=", str(round(100 * float(row["net"])) / 100),
            #           "is_short", str(row["is_short"]),
            #           "is_long=",str(row["is_long"])
            #           )

            if strategy_name not in dic:
                dic[strategy_name] = {"position": {}, "charts": {}}

            # for timestamp, row in self.strategies[strategy_name].position.log_position_status.iterrows():
            #     print(timestamp, row.tolist())
            #
            print(self.strategies[strategy_name].position.log_position_status)
            #

            # print(self.strategies[strategy_name].position.rpnl)

            row = self.strategies[strategy_name].position.log_position_status.iloc[-1]
            # print(row.tolist())

            dic[strategy_name]["position"]["rpnl"] = str(round(100 * float(row["rpnl"])) / 100)
            dic[strategy_name]["position"]["upnl"] = str(round(100 * float(row["upnl"])) / 100)
            # print(strategy_name, "\n", dic[strategy_name])

            dic[strategy_name]["charts"]['mean_prices'] = self.strategies[strategy_name].position.get_chart_data(
                ['spsm', 'lpsm'], scale=1)

            # dic[strategy_name]["charts"]['mean_returns'] = self.strategies[strategy_name].position.get_chart_data(
            #     ['last_returns_mean', 'returns_mean'], scale=100)
            dic[strategy_name]["charts"]['close_price'] = self.strategies[strategy_name].position.get_chart_data(
                ['close_price'], scale=1)

            dic[strategy_name]["charts"]['z_score'] = self.strategies[strategy_name].position.get_chart_data(
                ['z_score'], scale=1)

            dic[strategy_name]["charts"]['net'] = self.strategies[strategy_name].position.get_chart_data(
                ['net'], scale=1)

            # print(dic[strategy_name]["charts"]['net'])

            # print(strategy_name, "\n", dic[strategy_name])

            # for k in dic[strategy_name]["charts"]:
            #     print(k, "\n", dic[strategy_name]["charts"][k])

        print('Backtest completed.')
        # print(dic)
        return dic

# ---------------------------------
class StrategyAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90004-000-1 StrategyAlgo", dic, '\n', '-'*50)
        try:
            super(StrategyAlgo, self).__init__()
        except Exception as ex:
            print("Error 90004-010-1 StrategyDataProcessing:\n"+str(ex), "\n", '-'*50)
        # print("90004-020-1 StrategyAlgo", dic, '\n', '-'*50)


class StrategyDataProcessing(BaseDataProcessing, BasePotentialAlgo, StrategyAlgo):
    def __init__(self, dic):
        super().__init__(dic)

    def test(self, dic):
        print("90300-600-545: \n", "="*50, "\n", dic, "\n", "="*50)

        app_ = dic["app"]
        years_ = float(dic["years"])
        tickers = dic["tickers"] # ["AAPL"] # "AAPL", "MSFT", "GOOG", "2223.SR","NVDA", "ALT", "NICE", "MNDY"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(365*years_))
        # end_date = end_date - timedelta(days=365 * 1)
        print("end=", str(end_date.date()), " start=", str(start_date.date()), "\n", "="*50, "\n")
        start_date_ = start_date.year*10000+start_date.month*100+start_date.day
        end_date_ = end_date.year*10000+end_date.month*100+end_date.day
        # print(start_date_, end_date_)
        results = {}
        # model_company_info = apps.get_model(app_label=app_, model_name="companyinfo")
        model_stockpricesdays = apps.get_model(app_label=app_, model_name="stockpricesdays")

        for ticker_ in tickers:
            # # From Yahoo
            # df = yf.download(ticker_, start_date, end_date)
            # df_ = df.drop('Close', 1).rename(columns={"Adj Close": "Close"})
            # print("\n", "="*100, "\n", ticker_, "\n", "="*100, "\n")
            # print("BBBB\n", df_)
            # #
            qs = model_stockpricesdays.objects.filter(company__ticker=ticker_,
                                                      idx__gte=start_date_, idx__lte=end_date_).all()
            df = pd.DataFrame(list(qs.values("idx", "open", "close", "high", "low", "volume")))
            df['idx'] = pd.to_datetime(df['idx'], format='%Y%m%d').dt.date
            df = df.set_index("idx")
            df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'}, inplace=True)
            df = df.sort_index(ascending=True)
            # print(ticker_, "\ndf\n", df)
            # =======================
            engine = BacktestEngine(symbol=ticker_, trade_qty=1, start=str(start_date.date()), end=str(end_date.date()), df=df)
            re_ = engine.start(dic)
            results[ticker_] = re_

        result = {"status": "ok", "results": results}
        # print(result)
        return result

