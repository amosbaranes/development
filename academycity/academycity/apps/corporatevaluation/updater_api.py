from ..corporatevaluation.xbrl_obj import AcademyCityXBRL

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_forecast, 'interval', minutes=60, id='update_earning_forecast')
    scheduler.start()


def update_forecast():
    try:
        nday = datetime.today().weekday()  # Monday = 0
        h = datetime.today().hour
        # print(h)
        if nday < 6:
            # and (h == 23 or h == 16)
            acx = AcademyCityXBRL()
            acx.get_earning_forecast_sp500()
            del acx
    except Exception as ex:
        print(ex)


