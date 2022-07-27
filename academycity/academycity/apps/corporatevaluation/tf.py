# https://www.investopedia.com/terms/c/cml.asp
# https://www.princeton.edu/~markus/teaching/Eco525/05%20CAPM_a.pdf   page 53
# https://www.investopedia.com/terms/c/capm.asp
#  homework: https://www2.isye.gatech.edu/~shackman/isye6225_Summer11/CapitalAssetPricingModelHomework.pdf

# https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/

import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

list_of_tickers = ['IBM', 'AAPL', 'GOOG']
XP = data.DataReader(list_of_tickers, 'yahoo', start='2020/01/01', end='2022/07/22')
# print("Prices-"*3)
# print("="*30)
# print(XP['Adj Close'])
# print("Prices-"*3)
X = XP['Adj Close'].pct_change().apply(lambda x: np.log(1+x))
print(X)
V = X.cov()

print(V)

# w = {'IBM': 0.1, 'AAPL': 0.3, 'GOOG': 0.6}
# PV = V.mul(w, axis=0).mul(w, axis=1).sum().sum()
# print(PV)

# print('-'*10)
# print(V.mul(w, axis=0))
# print('-'*10)
# print(V.mul(w, axis=1))
# print('-'*10)
# print(V.mul(w, axis=0).mul(w, axis=1))

xr = XP['Adj Close'].resample('Y').last().pct_change().mean()
print(xr)
print('xr-'*10)
w = [0.1, 0.3, 0.6]

pr = (w*xr).sum()
print('pr-'*10)
print(pr)
print('xsd-'*10)
xsd = X.std().apply(lambda x: x*np.sqrt(250))
print(xsd)

rv = pd.concat([xr, xsd], axis=1) # Creating a table for visualising returns and volatility of assets
rv.columns = ['Returns', 'Volatility']
print(rv)

i_r = []  # Define an empty array for portfolio returns
i_sd = []  # Define an empty array for portfolio volatility
i_w = []  # Define an empty array for asset weights

ns = len(X.columns)
nb = 10000
for i in range(nb):
    w = np.random.random(ns)
    w = w/np.sum(w)
    i_w.append(w)
    r = np.dot(w, xr)
    i_r.append(r)
    var = V.mul(w, axis=0).mul(w, axis=1).sum().sum()
    sd = np.sqrt(var) # Daily standard deviation
    sd = sd*np.sqrt(250) # Annual standard deviation = volatility
    i_sd.append(sd)

data = {'Returns': i_r, 'Volatility': i_sd}
for counter, symbol in enumerate(X.columns.tolist()):
    data['w'+symbol] = [w[counter] for w in i_w]

portfolios = pd.DataFrame(data)
print(portfolios)

portfolios.plot.scatter(x='Volatility', y='Returns', marker='o', s=10, alpha=0.3, grid=True, figsize=[10,10])
plt.show()

# Finding the optimal portfolio
rf = 0.01 # risk factor
optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
print(optimal_risky_port)

