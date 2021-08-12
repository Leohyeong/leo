import time
import pyupbit
import datetime
import pandas as pd

tickers = pyupbit.get_tickers(fiat="KRW")

balance = 598391*0.9995/102



for i in range(0,len(tickers)):
    data = pd.DataFrame(
    {
        'Coin': [tickers[i]],
        'balance': [balance]
    })

print(data)


