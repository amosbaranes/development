import asyncio
import datetime

from tda import auth, client
from tda.streaming import StreamClient
from ..core.utils import log_debug, clear_log_debug
import os
from django.conf import settings


class BaseTDAmeriTrade(object):
    def __init__(self):
        # clear_log_debug()
        self.PROJECT_ROOT_DIR = os.path.join(settings.WEB_DIR, "data", "corporatevaluation")
        os.makedirs(self.PROJECT_ROOT_DIR, exist_ok=True)

        self.TO_DATA_PATH = os.path.join(self.PROJECT_ROOT_DIR, "datasets")
        os.makedirs(self.TO_DATA_PATH, exist_ok=True)

        self.OPTIONS_PATH = os.path.join(self.PROJECT_ROOT_DIR, "options")
        os.makedirs(self.OPTIONS_PATH, exist_ok=True)
        #
        self.token_path = os.path.join(self.OPTIONS_PATH, "token")
        os.makedirs(self.token_path, exist_ok=True)
        #
        self.sp_tickers = None
        self.sp_tickers_list = ["SPX", "RUT", "IWM", "QQQ", "NDX", "SPY", "TSLAS", "PYPL", "AMZN", "BABA", "FB"]
        self.sp_tickers_str = None
        # need to move to env file
        self.password = "Sigal2105Shir930"
        self.user_name = "amosbaranes"
        self.callback_url = "https://academycity.org/en/corporatevaluation/options"
        self.app_name = "academycity"
        self.customer_key = "LLGYGYRSAMWGZJNMXY8B8KGTOYG9BNDU"
        self.api_key = self.customer_key + "@AMER.OAUTHAP"
        self.account_id = "252456363"
        #
        try:
            import shutil
            BIN_DIR = "/tmp/bin"
            if not os.path.exists(BIN_DIR):
                os.makedirs(BIN_DIR)
            CURR_BIN_DIR = self.token_path
            executable_name = "chromedriver"
            currfile = os.path.join(CURR_BIN_DIR, executable_name)
            newfile = os.path.join(BIN_DIR, executable_name)
            shutil.copy2(currfile, newfile)
            os.chmod(newfile, 0o775)
        except Exception as ex:
            print(ex)

    def get_stream_client(self):
        easy_client = auth.easy_client(api_key=self.customer_key, redirect_uri=self.callback_url,
                                       token_path=self.token_path + "/token", )
        return StreamClient(easy_client, account_id=self.account_id)

    def add_zero(self, s):
        if len(s) == 1:
            s = "0" + s
        return s

    def get_option_month_letter(self, option_type="C", n=1):
        n = n - 1
        if option_type == "P":
            n = n + 12
        ls_ = "ABCDEFGHIJKLMNOPQRSTUVWX"
        return ls_[n]

    async def read_several_stream(self, services):
        try:
            stream_client = self.get_stream_client()
            await stream_client.login()
            await stream_client.quality_of_service(StreamClient.QOSLevel.FAST)
        except Exception as ex:
            pass
            # print("Error Login: "+str(ex))

        for s_ in services:
            try:
                # print(s_)
                add_func = s_["add_func"]
                func = s_["func"]
                subs_func = s_["subs_func"]
                tickers = s_["tickers"]
                # print("stream_client." + add_func + "(" + func + ")")
                eval("stream_client." + add_func + "("+func+")")
                # print("Running:  await stream_client." + subs_func + "(['"+tickers+"'])")
                await eval("stream_client." + subs_func + "(['"+tickers+"'])")
            except Exception as ex:
                print(str(ex))

        # print("Start streaming")
        n_ = 2
        i = 0
        d = datetime.datetime.now()
        date_string_start = str(d.year)+"-"+self.add_zero(str(d.month))+"-" + self.add_zero(str(d.day))+" 16:30:00"
        date_string_end = str(d.year)+"-"+self.add_zero(str(d.month))+"-" + self.add_zero(str(d.day))+" 23:00:00"
        # print(datetime.datetime.fromisoformat(date_string_start), datetime.datetime.fromisoformat(date_string_end))

        d1 = datetime.datetime.now()
        # while datetime.datetime.fromisoformat(date_string_start) < d < datetime.datetime.fromisoformat(date_string_end):
        while True:
            await stream_client.handle_message()
            await asyncio.sleep(6)
            d = datetime.datetime.now()
