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

def backtest(name,days,k):
    
    df = pyupbit.get_ohlcv(name,count=days)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror_tempt'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'] - fee,
                            1)
    df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

    df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                        df['close'] / df['target'] - fee,
                        1) - 1)
    df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

    df['dd'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)
    print("MDD(%): ", df['dd'].max())
    # df.to_excel("dd.xlsx")

    print(df)

backtest(name,days,best_k)

## Auto Trade ##

# # KRW로 표기된 종목의 코드 확인
tickers = pyupbit.get_tickers(fiat="KRW")
print(len(tickers))

# 102개 5천원 

aaa = 102 * 5000

print(aaa)
