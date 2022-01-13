from ..corporatevaluation.xbrl_obj import AcademyCityXBRL
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

    except Exception as ex:
        pass
        # print(ex)


