from ..corporatevaluation.xbrl_obj import AcademyCityXBRL

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
        # print(nday)
        acx = AcademyCityXBRL()
        if nday < 6:
            # and (h == 23 or h == 16)
            # print('update_forecast 1')
            acx.get_earning_forecast_sp500()
            del acx
        # elif nday == 6:
        #     if h == 4:
        #         acx.get_announcement_time("1")
        #     if h == 5:
        #         acx.get_announcement_time("2")
        #     if h == 6:
        #         acx.get_announcement_time("3")

    except Exception as ex:
        pass
        # print(ex)


