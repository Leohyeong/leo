import time
import pyupbit
import telegram
import math
import datetime

bot = telegram.Bot(token='1825271568:AAHLOTqYV8ZZ8IN0I1N-FpR68g0PGThQyVs')
chat_id = 1893587930

fee = 0.9995

## __KRW_coin__ ##

krw_etc = "KRW-ETC"

## __coin_name__ ##

etc = "ETC"

## __k_coin__ ##

k_etc = 0.1

## __min_val__ ##

etc_min = 0.043

## function ##

def get_target_price(ticker, k):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
    # 시가 + 변동폭

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
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]



## 로그인 ##

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"

upbit = pyupbit.Upbit(access, secret)


print("* Etherium Classic Trading *")


# 자동매매 시작
while True:

    try:
        now = datetime.datetime.now()
        start_time = get_start_time(krw_etc)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            mybalance = float(math.floor(upbit.get_balance('KRW')))
            target_price = get_target_price(krw_etc, k_etc)
            current_price = get_current_price(krw_etc)
            etc_coin = get_balance(etc)
            if (mybalance > 5000) & (etc_coin < etc_min):
                if target_price <= current_price:
                        upbit.buy_market_order(krw_etc, mybalance*fee)
                        mybalance = float(round((mybalance * fee),-1))
                        print("Buy :", etc ," price :", str(mybalance))
                        bot.sendMessage(chat_id=chat_id, text="Buy : "+etc+" price : "+str(mybalance))
        else:
            etc_coin = get_balance(etc)
            if etc_coin > etc_min:
                upbit.sell_market_order(krw_etc, etc_coin)
                mybalance = float(math.floor(etc_coin*current_price))
                print("Sell :", etc, " price :", str(mybalance))
                bot.sendMessage(chat_id=chat_id, text="Sell : "+etc+" price : "+str(mybalance))
    except Exception as e:
        print(e)
        time.sleep(1)
