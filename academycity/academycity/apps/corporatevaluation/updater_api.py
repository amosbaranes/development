from ..corporatevaluation.objects import AcademyCityXBRL, StockPrices
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
            elif h == 3:
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


