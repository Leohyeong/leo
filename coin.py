import time
import pyupbit
import telegram
import math

bot = telegram.Bot(token='1825271568:AAHLOTqYV8ZZ8IN0I1N-FpR68g0PGThQyVs')
chat_id = 1893587930


fee = 0.9995

## __KRW_coin__ ##

krw_eth = "KRW-ETH"

## __coin_name__ ##

eth = "ETH"

## __min_val__ ##

eth_min = 0.0014

## function ##

def get_ma20(ticker):
    """20분 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


def coin_autotrade(__krw_coin__,__coin_name__,__min_val__,__money__):
    try:
        ma20 = get_ma20(__krw_coin__)
        current_price = get_current_price(__krw_coin__)
        coin = get_balance(__coin_name__)
        if (ma20 <= current_price <= ma20+5000):
            if (__money__ > 5000) & (coin < __min_val__):
                upbit.buy_market_order(__krw_coin__, __money__*fee)
                __money__ = float(round((__money__ * fee),-1))
                print("Buy :", __coin_name__ ," price :", str(current_price))
                bot.sendMessage(chat_id=chat_id, text="Buy : "+__coin_name__+" price : "+str(__money__))
        elif (ma20-6000 > current_price):
            if (coin > __min_val__):
                upbit.sell_market_order(__krw_coin__, coin)
                __money__ = float(coin * get_current_price(__krw_coin__))
                print("Sell :", __coin_name__ ," price :", str(current_price))
                bot.sendMessage(chat_id=chat_id, text="Sell : "+__coin_name__+" price : "+str(__money__))
    except Exception as e:
        print(e)
        time.sleep(1)
    
    return __money__


## 로그인 ##

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"

upbit = pyupbit.Upbit(access, secret)

mybalance = float(math.floor(upbit.get_balance('KRW')))

eth_val = mybalance

print("ETH Trading...")


# 자동매매 시작

while True:

    eth_val = coin_autotrade(krw_eth,eth,eth_min,eth_val)
