from ...ml.basic_ml_objects import BaseDataProcessing, BasePotentialAlgo
from ....core.utils import log_debug, clear_log_debug
#
import wbdata
# import world_bank_data as wb
try:
    import pandasdmx as sdmx
except Exception as ex:
    print("ERROR:", ex)

import requests
import wbgapi as wb
import pandas as pd
import datetime
import openai
from openai import OpenAI



import os
import io
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class RDAlgo(object):
    def __init__(self, dic):  # to_data_path, target_field
        # print("90567-8-000 Algo\n", dic, '\n', '-'*50)
        try:
            super(RDAlgo, self).__init__()
        except Exception as ex:
            print("Error 9057-010 Algo:\n"+str(ex), "\n", '-'*50)
        # print("MLAlgo\n", self.app)
        # print("90004-020 DNQAlgo\n", dic, '\n', '-'*50)
        self.app = dic["app"]

    def get_world_bank_data(self, country_code, indicator):
        # indicator=SP.POP.TOTL
        base_url = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json"
        response = requests.get(base_url.format(country_code, indicator))
        data = response.json()[1]  # Get the population data from the response
        # print(data)

        # a = [{'indicator': {'id': 'SP.POP.TOTL', 'value': 'Population, total'},
        #       'country': {'id': 'IL', 'value': 'Israel'},
        #       'countryiso3code': 'ISR',
        #       'date': '2023',
        #       'value': 9756700,
        #       'unit': '', 'obs_status': '', 'decimal': 0},
        #      {'indicator': {'id': 'SP.POP.TOTL', 'value': 'Population, total'},
        #       'country': {'id': 'IL', 'value': 'Israel'}, 'countryiso3code': 'ISR', 'date': '2022',
        #       'value': 9557500, 'unit': '', 'obs_status': '', 'decimal': 0}
        #      ]
        a = [(x['countryiso3code'], x['country']['value'], x['indicator']['id'], x['date'], x['value']) for x in data]
        # print(a)
        return a

    def chat_with_gpt(self, messages):
        client = OpenAI()
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="gpt-3.5-turbo",
            )
            print(chat_completion)
            return chat_completion.choices[0].message['content'].strip()
        except Exception as ex_:
            print("Rate limit exceeded. Waiting before retrying...")
            print(ex_)
        return {"error": -1}


class RDDataProcessing(BaseDataProcessing, BasePotentialAlgo, RDAlgo):
    def __init__(self, dic):
        # print("90567-010 DataProcessing\n", dic, '\n', '-' * 50)
        super().__init__(dic)
        # print("9005 DataProcessing ", self.app)

    def upload_data(self, dic):
        print("90155-rd: \n", "="*50, "\n", dic, "\n", "="*50)

        # https://blogs.worldbank.org/en/opendata/introducing-wbgapi-new-python-package-accessing-world-bank-data
        x = "B"
        if x == "A":
            # Set the date range for the data
            start_date = datetime.datetime(2010, 1, 1)
            end_date = datetime.datetime(2020, 1, 1)

            print(start_date)

            # Define indicators (GDP growth, debt-to-GDP ratio, unemployment)
            indicators = {
                'NY.GDP.MKTP.KD.ZG': 'GDP Growth (%)',  # GDP growth (annual %)
                'GC.DOD.TOTL.GD.ZS': 'Debt-to-GDP (%)',  # Total government debt (% of GDP)
                'SL.UEM.TOTL.ZS': 'Unemployment Rate (%)'  # Unemployment (% of total labor force)
            }

            try:
                countries = wb.economy.info()
                print("AA\n", "="*1000, "\n", countries)
                # countries_df = pd.DataFrame(countries)

            except Exception as ex:
                print(ex)

            # Get data for a specific country (or use 'all' for multiple countries)
            countries = ['USA', 'ISR']  # Example: United States (ISO country code)

            # Fetch data
            try:
                df = wbdata.get_dataframe(indicators, country=countries)
                print(df)
            except Exception as ex:
                print(ex)

            # # Data Cleanup
            # df.reset_index(inplace=True)
            # # Display data
            # print(df.head())
            #
            # # Plot GDP Growth over time
            # df.plot(x='date', y='GDP Growth (%)', kind='line', title='GDP Growth Over Time')
        elif x == "B":
            # https://quant-trading.co/how-to-download-data-oecd-database/
            # https://www.oecd-ilibrary.org/economics/data/main-economic-indicators/main-economic-indicators-complete-database_data-00052-en#:~:text=The%20Main%20Economic%20Indicators%20database,foreign%20finance%2C%20foreign%20trade%2C%20and

            # database = '@DF_FINMARK,4.0'
            # country_code = 'USA+JPN+DEU'
            # frequency = 'M'
            # indicator = 'IRLT'
            # unit_of_measure = 'PA'
            # start_period = '1955-01'

            database = '@DF_CLI'
            country_code = 'JPN+DEU+FRA+CAN+AUS'
            frequency = 'M'
            indicator = 'LI..'
            unit_of_measure = 'AA...'
            start_period = '2023-01'

            query_text = database + "/" + country_code + "." + frequency + "." + indicator + "." + unit_of_measure + ".....?startPeriod=" + start_period + "&dimensionAtObservation=AllDimensions"

            url = f"https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES{query_text}"
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.sdmx.data+csv; charset=utf-8'}

            download = requests.get(url=url, headers=headers)
            df2 = pd.read_csv(io.StringIO(download.text))
            print(df2[["REF_AREA", "TIME_PERIOD","OBS_VALUE"]])

        # technology: GB.XPD.RSDV.GD.ZS  population: SP.POP.TOTL
        # a = self.get_world_bank_data("ISR", "SP.POP.TOTL")
        # print(a)

        # a = self.get_world_bank_data("ISR", "GB.XPD.RSDV.GD.ZS")
        # print(a)
        #

        #
        # company = "Google"
        # prompt = f"Analyze the financial data of {company} and suggest a reasonable FCF growth rate, WACC, and terminal growth rate."
        # result = self.ask_o1(prompt)
        # print(result)
        #

        messages = [
            {"role": "user",
             "content": "Say this is a test",
            }]

        # self.chat_with_gpt(messages)

        result = {"status": "ok rd"}
        return result

