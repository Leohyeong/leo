import time
import pyupbit
import datetime
import pandas as pd
import math
import numpy as np

tickers = pyupbit.get_tickers(fiat="KRW")

start_day = datetime(2021,8,10)
today = datetime.now()
days = days = (today-start_day).days

access = "xYEholhmUOxsVOLoAh6NdxE0HQT2meKq4nxBUaXB"
secret = "Kny70chrbB0d8x9x1hdmNgclVqepcUuxo4YZDoco"

upbit = pyupbit.Upbit(access, secret)

fee = 0.0005

balance = float(math.floor(upbit.get_balance('KRW')*(1-fee)/len(tickers)))

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
def coin_data():
    df = pd.DataFrame(
        {
            'coin': [tickers[0]],
            'balance': [balance],
            'name' : [tickers[0][tickers[0].find('-')+1:]],
            'min_num' : [5000/get_current_price(tickers[0])]
        }
    )

    for i in range(1,len(tickers)):
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


def get_target_price(ticker, k):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma20(coin):
        """20시간 이동 평균선 조회"""
        df = pyupbit.get_ohlcv(coin, interval="day", count=20)
        ma20 = df['close'].rolling(20).mean().iloc[-1]
        bol_lower = ma20 - 2*df['close'].rolling(20).std().iloc[-1]
        return bol_lower

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
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



time.sleep(0.1)

coin = get_balance("DOGE")

current_price = get_current_price("KRW-DOGE")
print(balance)
print(current_price)
print(coin)

# # 자동매매 시작

def coin_autotrade(__krw_coin__,__k_coin__,__coin_name__,__min_val__,__money__):
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(__krw_coin__)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=59):
            target_price = get_target_price(__krw_coin__, __k_coin__)
#             ma20 = get_ma20(__krw_coin__)
            current_price = get_current_price(__krw_coin__)
            if target_price < current_price:
                coin = get_balance(__coin_name__)
                if __money__ > 5000 and coin < __min_val__:
                    upbit.buy_market_order(__krw_coin__, __money__*fee)
                    __money__ = int(round((__money__ * fee),-1))
                    # print("Buy :", __coin_name__ ," price :", str(__money__))
                    bot.sendMessage(chat_id=chat_id, text="Buy : "+__coin_name__+" price : "+str(__money__))
        else:
            coin = get_balance(__coin_name__)
            if coin > __min_val__:
                upbit.sell_market_order(__krw_coin__, coin)
                __money__ = coin * get_current_price(__krw_coin__)
                # print("Sell :", __coin_name__ ," price :", str(__money__))
                bot.sendMessage(chat_id=chat_id, text="Sell : "+__coin_name__+" price : "+str(__money__))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
    
    return __money__


for i in range(0,len(tickers)):
    coin_autotrade(tickers[i],best_k[i],__coin_name__,__min_val__,__money__)
