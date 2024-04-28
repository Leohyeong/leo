import pyupbit
import numpy as np
import time
from datetime import datetime
import pandas as pd

start_time = datetime.now()

tickers = pyupbit.get_tickers(fiat="KRW")

start_day = datetime(2021,8,10)
today = datetime.now()
days = days = (today-start_day).days

################################################ Function ################################################


def backtest_and_bestk(ticker,days):

    def get_ma20(coin):
        """20시간 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(coin, interval="day", count=20)
        ma20 = df['close'].rolling(20).mean().iloc[-1]
        bol_lower = ma20 - 2*df['close'].rolling(20).std().iloc[-1]
        return bol_lower

    def get_ror(ticker,k=0.5):
        df = pyupbit.get_ohlcv(ticker,interval="day",count=200)
        time.sleep(0.3)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0005
        df['ror'] = np.where((df['high'] > df['target']) & (get_ma20(ticker) >= df['close']),
                            df['close'] / df['target'] - fee,
                            1)

        ror = df['ror'].cumprod()[-2]
        return ror

    k_tmp = []

    for i in range(9):
        k_tmp.append(0)

    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(ticker,k)
        a = int(k*10-1)
        k_tmp[a] = ror
        # print("%.1f %f" % (k, ror))

    best_k = (k_tmp.index(max(k_tmp))+1)*0.1  
    print(str(ticker) +" best k value : " + str(round(best_k,2)))

    def backtest(ticker,k,days):
        
        df = pyupbit.get_ohlcv(ticker,interval="day",count=days)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0005
        df['ror_tempt'] = np.where((df['high'] > df['target']) & (get_ma20(ticker) >= df['close']),
                                df['close'] / df['target'] - fee,
                                1)
        df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

        df['ror'] = 100 * (np.where((df['high'] > df['target']) & (get_ma20(ticker) >= df['close']), # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                            df['close'] / df['target'] - fee,
                            1) - 1)
        df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

        df['dd'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

        mdd = round(df['dd'].max(),1)
        print("MDD(%): ", mdd)
        
        hpr = round(df['hpr'].iloc[-1],1)
        print("hpr(%): ", hpr, "\n")

        print(df)

        return hpr, mdd


    hpr_mdd = backtest(ticker,best_k,days)

    data = pd.DataFrame(
    {
        'Coin': [ticker],
        'k': [best_k],
        'hpr': [hpr_mdd[0]],
        'MDD': [hpr_mdd[1]]
    })

    return data
    
################################################ Backtest ################################################

print("\nNo. " + str(1))
df = backtest_and_bestk(tickers[0],days)


for i in range(1,len(tickers)):
    print("No. " + str((i+1)))
    new_data = backtest_and_bestk(tickers[i],days)
    df = df.append(new_data)
    time.sleep(0.1)

df.to_excel(str(datetime.now().strftime('%Y-%m-%d'))+"_d"+str(days)+'.xlsx',index=False)

################################################ Time lapse ################################################
def info_time():
    print("\nstart time : " + start_time.strftime('%H:%M:%S'))

    end_time = datetime.now()

    print("end time : " + end_time.strftime('%H:%M:%S'))

    gap = end_time - start_time

    print("Total time lapse : " + str(gap))

info_time()
