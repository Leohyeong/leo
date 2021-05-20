import time
import pyupbit
import telegram
import math

bot = telegram.Bot(token='1825271568:AAHLOTqYV8ZZ8IN0I1N-FpR68g0PGThQyVs')
chat_id = 1893587930


fee = 0.9995

## __KRW_coin__ ##

krw_doge = "KRW-DOGE"

## __coin_name__ ##

doge = "DOGE"

## eth_min ##

doge_min = 10.2

## function ##

def get_ma20(ticker):
    """20분 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def ma_grad(ticker):
    """이동평균선 기울기"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
    ma = df['close'].rolling(20).mean().iloc[-1]-df['close'].rolling(20).mean().iloc[-2]
    return ma

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

## 로그인 ##

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"

upbit = pyupbit.Upbit(access, secret)


print("DOGE Trading...")


# 자동매매 시작

while True:

    try:

        mybalance = float(math.floor(upbit.get_balance('KRW')))
        ma20 = get_ma20(krw_doge)
        ma = ma_grad(krw_doge)
        current_price = get_current_price(krw_doge)
        coin = get_balance(doge)
        if (ma > 0) & (ma20 < current_price <= ma20+3):
            if (mybalance > 5000) & (coin < doge_min):
                upbit.buy_market_order(krw_doge, mybalance*fee)
                mybalance = float(round((mybalance * fee),-1))
                print("Buy :", doge ," price :", str(mybalance))
                bot.sendMessage(chat_id=chat_id, text="Buy : "+doge+" price : "+str(mybalance))
        elif (ma20-3 > current_price):
            if (coin > doge_min):
                upbit.sell_market_order(krw_doge, coin)
                mybalance = float(math.floor(coin*current_price))
                print("Sell :", doge, " price :", str(mybalance))
                bot.sendMessage(chat_id=chat_id, text="Sell : "+doge+" price : "+str(mybalance))
    except Exception as e:
        print(e)
    time.sleep(1)
