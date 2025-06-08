from ..corporatevaluation.objects import AcademyCityXBRL, FinancialAnalysis, StockPrices, CorporateValuationDataProcessing
from ..corporatevaluation.models import XBRLRealEquityPrices
from ..core.sql import SQL
from ..core.utils import log_debug, clear_log_debug

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    # print('start')
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_forecast, 'interval', minutes=60, id='update_earning_forecast')
    scheduler.start()

def update_forecast():
    try:
        clear_log_debug()
    except Exception as ex:
        pass
    h = 0
    try:
        nday = datetime.today().weekday()  # Monday = 0
        h = datetime.today().hour
        # print(h)
        acx = AcademyCityXBRL()
        if nday < 6:
            if h == 1:
                print("1.A hour 1"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("1.A hour 1"+str(datetime.today().hour)+str(datetime.today().minute))
                data = ()
                ssql = " insert into corporatevaluation_XBRLRealEquityPricesArchive(ticker,t,o,h,l,c,v) "
                ssql += "select ticker,t,o,h,l,c,v from corporatevaluation_XBRLRealEquityPrices"
                count = SQL().exc_sql(ssql, data)
                XBRLRealEquityPrices.truncate()
                print("1.B hour 1"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("1.B hour 1"+str(datetime.today().hour)+str(datetime.today().minute))
            elif h == 4:
                print("2.A hour 4"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("2.A hour 4"+str(datetime.today().hour)+str(datetime.today().minute))
                sp = StockPrices()
                # print("Start Days")
                try:
                    dic = {"letter_from": "A", "letter_to": "Z", "numer_of_years": 1, "numer_of_days": 3}
                    sp.update_prices_days(dic)
                except Exception as ex:
                    print("m - " + str(ex))
                # print("Start Minutes")
                print("2.A-1 hour 4"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("2.A-1 hour 4"+str(datetime.today().hour)+str(datetime.today().minute))
                try:
                    dic = {"letter_from": "A", "letter_to": "Z", "numer_of_weeks": 1, "numer_of_days": 1}
                    sp.update_prices_minutes(dic)
                except Exception as ex:
                    print("m - "+str(ex))
                del sp
                print("2.B hour 4 "+str(datetime.today().hour)+":"+str(datetime.today().minute))
                log_debug("2.B hour 4"+str(datetime.today().hour)+":"+str(datetime.today().minute))
            elif h == 8:
                print("3.A hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("3.A hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
                fa = FinancialAnalysis()
                fa.update_time()
                print("Start 1")
                # dp = CorporateValuationDataProcessing(dic={"app":"corporatevaluation","topic_id":"general"})
                # # print("Start 11")
                # dp.data_transfer_to_process_fact(dic={"app":"corporatevaluation"})
                # # print("Start 12")
                # dp.create_new_group_accounts(dic={"app":"corporatevaluation",
                #                                   "aggregate_accounts":[11057, 11400, 11600, 11990, 12990, 12999,
                #                                                         13990,14100, 14145, 14999, 15390, 15990,
                #                                                         20100, 20200, 20300, 20700, 20800, 20850,
                #                                                         20900, 20970,20999],
                #                                   "new_accounts":{11991: {"add": [11990], "subtract": [11100]},
                #                                                   20997: {"add": [20999, 20850], "subtract": []},
                #                                                   20890: {"add": [20851], "subtract": [20850]}}
                #                                   })
                # # print("Start 3")
                # dp.create_ratios(dic={"app":"corporatevaluation"})
                # # print("End End End End End End End End ")
                print("3.B hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("3.B hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
                # -----
                acx.update_release_date()
                acx.get_earning_forecast_sp500()
                del acx
                print("4.B hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
                log_debug("4.B hour 8"+str(datetime.today().hour)+str(datetime.today().minute))
            print("Runed update_forecast " + str(h))
            log_debug("Runed update_forecast " + str(h))
    except Exception as ex:
        log_debug("Error update_forecast " + str(h) + str(ex))
        # print(ex)

