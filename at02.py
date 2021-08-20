from hashlib import new
import time
import pyupbit
import datetime
import math
import pandas as pd
import numpy as np

n=2

program_start_time = datetime.datetime.now()
print(program_start_time.strftime('%H:%M:%S'))

## Time infromation ##
"""경과 시간 함수"""
def info_time(start):
    print("start time : " + start.strftime('%H:%M:%S'))

    end = datetime.datetime.now()

    print("end time : " + end.strftime('%H:%M:%S'))

    gap = end - start

    print("Total time lapse : " + str(gap))

## All coin import ##
""""모든 코인 & 수수료"""

tickers = pyupbit.get_tickers(fiat="KRW")
tickers_start = 6 * (n-1)
tickers_end = tickers_start + 6
tickers_length = 6

fee = 0.0005

## Login ##
"""로그인"""
access = "xYEholhmUOxsVOLoAh6NdxE0HQT2meKq4nxBUaXB"
secret = "Kny70chrbB0d8x9x1hdmNgclVqepcUuxo4YZDoco"
upbit = pyupbit.Upbit(access, secret)
print("* Login complete")

## Divide balance ##
"""잔고 배분"""
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

def divideBalance():
    num_div = len(tickers)
    for i in range(len(tickers)):
        if get_balance(tickers[i][tickers[i].find('-')+1:]) > 0:
            num_div -= 1
    balan = float(math.floor((upbit.get_balance('KRW')*(1-fee))/num_div))
    return balan

balance = divideBalance() # 잔고 배분 함수 실행
print(balance)
# balance = 20000 * (1 + fee)

## Coin data update ##
"""데이터 업데이트"""
def get_current_price(ticker):
    """현재가 조회"""
    # time.sleep(0.1)
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def coin_data(bal):
    
    cdf_in = pd.DataFrame()
    
    for i in range(tickers_start,tickers_end):
        num = get_balance(tickers[i][tickers[i].find('-')+1:])
        if  num > 0:
            bal_in = 0
        else:
            bal_in = bal
        new_data = pd.DataFrame(
            {
            'coin': [tickers[i]],
            'balance': [bal_in],
            'name' : [tickers[i][tickers[i].find('-')+1:]],
            'min_num' : [5000/get_current_price(tickers[i])]
            }
        )
        print(new_data)
        cdf_in = cdf_in.append(new_data)
        

    print("* Coin data update")
    info_time(program_start_time)
    return cdf_in

cdf_in = coin_data(balance) # 데이터 업데이트 함수 실행
cdf = cdf_in.copy()
# cdf = cdf.to_excel("cdf.xlsx")
# cdf = pd.read_excel("cdf.xlsx")

## k data update ##
"""k 값 업데이트"""
def get_bol_lower(ticker):
    """30일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    # time.sleep(0.1)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    bol_lower = ma20 - 2 * df['close'].rolling(20).std().iloc[-1]
    return bol_lower

def get_ma20(ticker):
    """30일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    # time.sleep(0.1)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def updateBestk(ticker):

    def get_ror(ticker,k=0.5):
            df = pyupbit.get_ohlcv(ticker,interval="day",count=200)
            time.sleep(0.1)
            df['range'] = (df['high'] - df['low']) * k
            df['target'] = df['open'] + df['range'].shift(1)

            df['ror'] = np.where(df['high'] > df['target'],
                                df['close'] / df['target'] - fee,
                                1)

            ror = df['ror'].cumprod()[-2]
            return ror
    # 메인 영역
    

    kdf_val = pd.DataFrame()
    
    for k in np.arange(0.01, 1.0, 0.01):

        ror = get_ror(ticker,k)
        new_kdf_val = pd.DataFrame(
            {
            'k': [k],
            'ror': [ror]
            }
        )
        kdf_val = kdf_val.append(new_kdf_val)

    best_k = kdf_val.loc[kdf_val['ror']==max(kdf_val['ror']),'k'].copy()
    print(best_k)
    
    return best_k

def updateBestk_bol(ticker):

    def get_ror(ticker,k=0.5):
            df = pyupbit.get_ohlcv(ticker,interval="day",count=200)
            time.sleep(0.1)
            df['range'] = (df['high'] - df['low']) * k
            df['target'] = df['open'] + df['range'].shift(1)

            df['ror'] = np.where(((df['high'] > df['target']) & (get_bol_lower(ticker)>df['open'])),
                                df['close'] / df['target'] - fee,
                                1)

            ror = df['ror'].cumprod()[-2]
            return ror

    kdf_val = pd.DataFrame()
    
    for k in np.arange(0.01, 1.0, 0.01):
        ror = get_ror(ticker,k)
        new_kdf_val = pd.DataFrame(
            {
            'k': [k],
            'ror': [ror]
            }
        )
        kdf_val = kdf_val.append(new_kdf_val)

    best_k = kdf_val.loc[kdf_val['ror']==max(kdf_val['ror']),'k'].copy()
    print(best_k)
    
    return best_k

def assignk():
    kdf_in = pd.DataFrame()

    for i in range(tickers_start,tickers_end): # len(tickers)
        new_kdf = pd.DataFrame(
            {
            'k' :updateBestk(tickers[i])
            }
        )
        kdf_in = kdf_in.append(new_kdf)

    print("* K data update")
    kdf1 = kdf_in.copy()
    print(kdf1)
    return kdf1

def assignk_bol():
    kdf_in = pd.DataFrame()

    for i in range(tickers_start,tickers_end): # len(tickers)
        new_kdf = pd.DataFrame(
            {
            'k' :updateBestk_bol(tickers[i])
            }
        )
        kdf_in = kdf_in.append(new_kdf)

    print("* k_bol data update")
    kdf1 = kdf_in.copy()
    print(kdf1)
    return kdf1

ma20 = get_ma20("KRW-BTC")

if get_current_price("KRW-BTC") > ma20:
    kdf = assignk()
else:
    kdf_bol = assignk_bol()

# kdf = pd.read_excel("kdf.xlsx")


## Function ##

def get_target_price(ticker, k_val):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # time.sleep(0.001)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k_val
    return target_price

def get_open_price(ticker):
    df = pyupbit.get_ohlcv(ticker,interval="day",count=1)
    # time.sleep(0.1)
    open_price = df.iloc[0]['open']
    return open_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    # time.sleep(0.1)
    start_time = df.index[0]
    return start_time

def autotrade_buy(ticker,k_buy,name,min_num,balance):
    try:

        target_price = get_target_price(ticker, k_buy)
        current_price = get_current_price(ticker)
        num = get_balance(name)

        if target_price <= current_price <= target_price * 1.005: ## 목표 단가에 매수
            if (balance > 5000) & (num < min_num):
                upbit.buy_market_order(ticker, balance * (1-fee))
                balance = int(round(balance*(1-fee),-1))
                print("Buy :", name ," price :" , balance)

    except Exception as e:
        print(e)
        time.sleep(0.1)

    return balance

def autotrade_buy_bol(ticker,k_buy,name,min_num,balance):
    try:

        target_price = get_target_price(ticker, k_buy)
        current_price = get_current_price(ticker)
        num = get_balance(name)
        bol_lower = get_bol_lower(ticker)
        open = get_open_price(ticker)

        if (target_price <= current_price <= target_price * 1.005) & (bol_lower > open): ## 목표 단가에 매수
            if (balance > 5000) & (num < min_num):
                upbit.buy_market_order(ticker, balance * (1-fee))
                balance = int(round(balance*(1-fee),-1))
                print("Buy_bol :", name ," price :" , balance)

    except Exception as e:
        print(e)
        time.sleep(0.1)

    return balance

def autotrade_sell(ticker,name,min_num):
    try:
        num = get_balance(name)
        balance = 0
        if num > min_num:
            upbit.sell_market_order(ticker, num)
            balance = num * get_current_price(ticker)
            print("Sell :", name ," price :", balance)

        # time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(0.1)
    
    return balance

## AutoTrade ##

print("* Auto trade start")

info_time(program_start_time)

k_count = 1
myBalance = []
for i in range(tickers_length):
    myBalance.append(0)

while True:
    try:
        
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)   
        
        if start_time < now < end_time - datetime.timedelta(minutes=4):
                time.sleep(0.1)
                i = 0
                for i in range(tickers_length):
                    open_price = get_open_price(cdf.iloc[i]['coin'])
                    ma20 = get_ma20(cdf.iloc[i]['coin'])
                    if open_price > ma20:
                        myBalance[i] = autotrade_buy(cdf.iloc[i]['coin'],kdf.iloc[i]['k'],cdf.iloc[i]['name'],cdf.iloc[i]['min_num'],cdf.iloc[i]['balance'])
                        print(cdf.iloc[i]['coin'])
                    else:
                        myBalance[i] = autotrade_buy_bol(cdf.iloc[i]['coin'],kdf.iloc[i]['k'],cdf.iloc[i]['name'],cdf.iloc[i]['min_num'],cdf.iloc[i]['balance'])            
                if k_count == 0:
                    k_count = 1

        else:
            i = 0
            for i in range(tickers_length):
                myBalance[i] = autotrade_sell(cdf.iloc[i]['coin'],cdf.iloc[i]['name'],cdf.iloc[i]['min_num'])
                # time.sleep(0.1)
            if k_count == 1:
                if get_current_price("KRW-BTC") > get_ma20("KRW-BTC"):
                    kdf = assignk()
                else:
                    kdf_bol = assignk_bol()
                k_count = 0   

        time.sleep(0.2)

    except Exception as e:
        print(e)
        time.sleep(0.2)
