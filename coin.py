import time
import pyupbit
import telegram

bot = telegram.Bot(token='1825271568:AAHLOTqYV8ZZ8IN0I1N-FpR68g0PGThQyVs')
chat_id = 1893587930

mybalance = 727990/2

fee = 0.9995

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"


doge_val = mybalance
etc_val = mybalance
xrp_val = mybalance

## __KRW_coin__ ##

krw_doge = "KRW-DOGE"
krw_etc = "KRW-ETC"
krw_xrp = "KRW-XRP"


## __coin_name__ ##

doge = "DOGE"
etc = "ETC"
xrp = "XRP"

## __min_val__ ##

doge_min = 7.7
etc_min = 0.043
xrp_min = 2.92


## trade_time_set ##

trade_minute1 = "minute1"
trade_minute60 = "minute60"
trade_minute40 = "minute240"


## function ##

def get_ma20(ticker):
    """20시간 이동 평균선 조회"""
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

        if ma20 < current_price:
            coin = get_balance(__coin_name__)
            if __money__ > 5000 and coin < __min_val__:
                upbit.buy_market_order(__krw_coin__, __money__*fee)
                __money__ = int(round((__money__ * fee),-1))
                print("Buy :", __coin_name__ ," price :", str(__money__))
                bot.sendMessage(chat_id=chat_id, text="Buy : "+__coin_name__+" price : "+str(__money__))
        else:
            coin = get_balance(__coin_name__)
            if coin > __min_val__:
                upbit.sell_market_order(__krw_coin__, coin)
                __money__ = coin * get_current_price(__krw_coin__)
                print("Sell :", __coin_name__ ," price :", str(__money__))
                bot.sendMessage(chat_id=chat_id, text="Sell : "+__coin_name__+" price : "+str(__money__))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
    
    return __money__


## 로그인 ##

upbit = pyupbit.Upbit(access, secret)

print("Auto Trade Start!!!")


# 자동매매 시작

while True:

    doge_val = coin_autotrade(krw_doge,doge,doge_min,doge_val)

    etc_val = coin_autotrade(krw_etc,etc,etc_min,etc_val)

#     xrp_val = coin_autotrade(krw_xrp,xrp,xrp_min,xrp_val)
