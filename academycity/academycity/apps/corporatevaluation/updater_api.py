from ..corporatevaluation.objects import AcademyCityXBRL, FinancialAnalysis, StockPrices, CorporateValuationDataProcessing
from ..corporatevaluation.models import XBRLRealEquityPrices
from ..core.sql import SQL

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    # print('start')
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_forecast, 'interval', minutes=60, id='update_earning_forecast')
    scheduler.start()


def update_forecast():
    try:
        nday = datetime.today().weekday()  # Monday = 0
        h = datetime.today().hour
        # print(h)
        acx = AcademyCityXBRL()
        if nday < 6:
            acx.get_earning_forecast_sp500()
            del acx
            if h == 1:
                data = ()
                ssql = " insert into corporatevaluation_XBRLRealEquityPricesArchive(ticker,t,o,h,l,c,v) "
                ssql += "select ticker,t,o,h,l,c,v from corporatevaluation_XBRLRealEquityPrices"
                count = SQL().exc_sql(ssql, data)
                XBRLRealEquityPrices.truncate()
            elif h == 5:
                print("Start")
                fa = FinancialAnalysis()
                fa.update_time()
                print("Start 1")
                dp = CorporateValuationDataProcessing(dic={"app":"corporatevaluation","topic_id":"general"})
                # print("Start 11")
                dp.data_transfer_to_process_fact(dic={"app":"corporatevaluation"})
                # print("Start 12")
                dp.create_new_group_accounts(dic={"app":"corporatevaluation",
                                                  "aggregate_accounts":[11057, 11400, 11600, 11990, 12990, 12999,
                                                                        13990,14100, 14145, 14999, 15390, 15990,
                                                                        20100, 20200, 20300, 20700, 20800, 20850,
                                                                        20900, 20970,20999],
                                                  "new_accounts":{11991: {"add": [11990], "subtract": [11100]},
                                                                  20997: {"add": [20999, 20850], "subtract": []},
                                                                  20890: {"add": [20851], "subtract": [20850]}}
                                                  })
                # print("Start 3")
                dp.create_ratios(dic={"app":"corporatevaluation"})
                # print("End End End End End End End End ")
            elif h == 4:
                sp = StockPrices()
                # print("Start Days")
                try:
                    dic = {"letter_from": "A", "letter_to": "Z", "numer_of_years": 1, "numer_of_days": 3}
                    sp.update_prices_days(dic)
                except Exception as ex:
                    print("m - " + str(ex))
                # print("Start Minutes")
                try:
                    dic = {"letter_from": "A", "letter_to": "Z", "numer_of_weeks": 1, "numer_of_days": 1}
                    sp.update_prices_minutes(dic)
                except Exception as ex:
                    print("m - "+str(ex))
                del sp
    except Exception as ex:
        pass
        # print(ex)

