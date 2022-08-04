from yahoofinancials import YahooFinancials
import pandas as pd

ticker = 'XLE'
yahoo_financials = YahooFinancials(ticker)
data = yahoo_financials.get_historical_price_data(start_date='2022-07-10',
                                                  end_date='2022-08-02',
                                                  time_interval='daily')
df = pd.DataFrame(data[ticker]['prices'])
df = df.drop('date', axis=1).set_index('formatted_date')
# d = df["formatted_date"]
# print(d.iloc[0])
# print(type(d.iloc[0]))

print(df)

# data = investpy.etfs.get_etfs(country='United States')
# for i, c in data.iterrows():
#     print(c["symbol"])
# print(data.columns)

# data = investpy.etfs.get_etf_information("XLE")

# data = investpy.get_stock_historical_data(stock='BA',
#                                           country='United States',
#                                           from_date='01/01/2018',
#                                           to_date='01/08/2022')

# data = investpy.get_etf_historical_data(etf='XLF',
#                                         country='United States', from_date='01/01/2015', to_date='29/07/2022')

# print(data)

