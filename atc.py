import time
import pyupbit
import datetime
import math
import pandas as pd
import numpy as np


def info_time(start):
    print("\nstart time : " + start.strftime('%H:%M:%S'))

    end = datetime.datetime.now()

    print("end time : " + end.strftime('%H:%M:%S'))

    gap = end - start

    print("Total time lapse : " + str(gap))

## All coin import ##

tickers = pyupbit.get_tickers(fiat="KRW")

## Date ##

start_day = datetime.datetime(2021,8,11)
today = datetime.datetime.now()
days = days = (today-start_day).days

## login ##

access = "xYEholhmUOxsVOLoAh6NdxE0HQT2meKq4nxBUaXB"
secret = "Kny70chrbB0d8x9x1hdmNgclVqepcUuxo4YZDoco"

upbit = pyupbit.Upbit(access, secret)

print("* Login complete")

## fee & div ##

fee = 0.0005

# div = float(math.floor(upbit.get_balance('KRW')*(1-fee)/len(tickers)))
div = float(math.floor(742000*(1-fee)/len(tickers)))

## Coin data update ##

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def coin_data(balance):
    
    df = pd.DataFrame()

    for i in range(len(tickers)):
        new_data = pd.DataFrame(
            {
            'coin': [tickers[i]],
            'balance': [balance],
            'name' : [tickers[i][tickers[i].find('-')+1:]],
            'min_num' : [5000/get_current_price(tickers[i])]
            }
        )
        time.sleep(0.1)
        df = df.append(new_data)

    return df

cdf = coin_data(div)

cdf1 = cdf.copy()

print("* Coin data update")

## k data update ##

def k_val(ticker):

    def get_ror(ticker,k=0.5):
            df = pyupbit.get_ohlcv(ticker,interval="day",count=200)
            time.sleep(0.1)
            df['range'] = (df['high'] - df['low']) * k
            df['target'] = df['open'] + df['range'].shift(1)

            fee = 0.0005
            df['ror'] = np.where(df['high'] > df['target'],
                                df['close'] / df['target'] - fee,
                                1)

            ror = df['ror'].cumprod()[-2]
            return ror

    kdf_val = pd.DataFrame()
    
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(ticker,k)
        new_kdf_val = pd.DataFrame(
            {
            'k': [k],
            'ror': [ror]
            }
        )
        kdf_val = kdf_val.append(new_kdf_val)

    # kdf.to_excel(ticker[ticker.find('-')+1:]+"_"+str(datetime.now().strftime('%Y-%m-%d'))+"_k_origin"+'.xlsx')
    best_k = kdf_val.loc[kdf_val['ror']==max(kdf_val['ror'])]['k']
    # best_k_float = float(best_k)
    # print(ticker ," k value : ", best_k_float)
    # info_time(start_time)

    return best_k

start_k_time = datetime.datetime.now()

kdf = pd.DataFrame()

for i in range(len(tickers)):
    # print("No. " + str((i+1)))
    new_kdf = pd.DataFrame(
        {
        'k' :k_val(tickers[i])
        }
    )
    kdf = kdf.append(new_kdf)
    # df.to_excel(tickers[i][tickers[i].find('-')+1:]+"_"+str(datetime.now().strftime('%Y-%m-%d'))+'.xlsx')

print("* K data update")
info_time(start_k_time)
k = kdf.copy()

## Function ##

def get_target_price(ticker, k):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    time.sleep(0.1)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    time.sleep(0.1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def autotrade_buy(ticker,k,name,min_num,balance):
    try:
        
        target_price = get_target_price(ticker, k)
        current_price = get_current_price(ticker)
        num = get_balance(name)
        
        if target_price < current_price < target_price * 1.01: ## 목표 단가에 매수
            # num = get_balance(name)
            if (balance > 5000) & (num < min_num):
                upbit.buy_market_order(ticker, balance * (1-fee))
                balance = int(round(balance*(1-fee),-1))
                print("Buy :", name ," price :" , balance)
            
        elif (num > min_num) & (target_price * 0.95 > current_price): ## 5퍼 하락시 매도
                upbit.sell_market_order(ticker, num)
                balance = num * get_current_price(ticker)
                print("Sell :", name ," price :", balance)

        time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(0.1)

    return balance

def autotrade_sell(ticker,name,min_num,balance):
    try:
        num = get_balance(name)
        if num > min_num:
            upbit.sell_market_order(ticker, num)
            balance = num * get_current_price(ticker)
            print("Sell :", name ," price :", balance)

        time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(0.1)
    
    return balance

## AutoTrade ##

print("* Auto trade start")

i = 0
count = 1

while True:
    try:
        
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(minutes=10):
            
            start = datetime.datetime.now()
            for i in range(len(tickers)):
                cdf1.iloc[i]['balance'] = autotrade_buy(cdf1.iloc[i]['coin'],k.iloc[i]['k'],cdf1.iloc[i]['name'],cdf1.iloc[i]['min_num'],cdf1.iloc[i]['balance'])
                i += 1
            count = 1

        else:
            for i in range(len(tickers)):
                cdf1.iloc[i]['balance'] = autotrade_sell(cdf1.iloc[i]['coin'],cdf1.iloc[i]['name'],cdf1.iloc[i]['min_num'],cdf1.iloc[i]['balance'])
                i += 1
            
            if count == 1:
                kdf = pd.DataFrame()
                for i in range(len(tickers)):
                    new_kdf = pd.DataFrame(
                        {
                        'k' :k_val(tickers[i])
                        }
                    )
                    kdf = kdf.append(new_kdf)
                print("* K data update")
                info_time(start_k_time)
                k = kdf.copy()
                count = 0                

        time.sleep(0.2)

    except Exception as e:
        print(e)
        time.sleep(0.2)
