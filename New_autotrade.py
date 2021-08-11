import pyupbit
import numpy as np
from datetime import date, datetime, timedelta

name = "KRW-DOGE"

start_day = datetime(2021,2,1)
today = datetime.now()
days = (today-start_day).days

## Best k ##

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv(name,count=days)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

k_tmp = []

for i in range(9):
    k_tmp.append(0)
 
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    a = int(k*10-1)
    k_tmp[a] = ror
    # print("%.1f %f" % (k, ror))

best_k = (k_tmp.index(max(k_tmp))+1)*0.1  

# print("\n" + str(best_k) + "\n")

## Auto Trade ##



# # KRW로 표기된 종목의 코드 확인
tickers = pyupbit.get_tickers(fiat="KRW")
print(len(tickers))

# 102개 5천원 

aaa = 102 * 5000

print(aaa)
