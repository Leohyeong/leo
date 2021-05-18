import time
import pyupbit
import datetime
import telegram

bot = telegram.Bot(token='1825271568:AAHLOTqYV8ZZ8IN0I1N-FpR68g0PGThQyVs')
chat_id = 1893587930

mybalance = 100280

fee = 0.9995

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"


doge_val = 96736
eth_val = mybalance
etc_val = 94123
xrp_val = 103300
ada_val = 101956
eos_val = 83619
xlm_val = 103621
hbar_val = 22977+78002
trx_val = 96324
bch_val = mybalance

## __KRW_coin__ ##

krw_doge = "KRW-DOGE"
krw_eth = "KRW-ETH"
krw_etc = "KRW-ETC"
krw_xrp = "KRW-XRP"
krw_ada = "KRW-ADA"
krw_eos = "KRW-EOS"
krw_xlm = "KRW-XLM"
krw_hbar = "KRW-HBAR"
krw_trx = "KRW-TRX"
krw_bch = "KRW-bch"

## __coin_name__ ##

doge = "DOGE"
eth = "ETH"
etc = "ETC"
xrp = "XRP"
ada = "ADA"
eos = "EOS"
xlm = "XLM"
hbar = "HBAR"
trx = "TRX"
bch = "BCH"

## __k_coin__ ##

k_doge = 0.3 # o
k_eth = 0.8  # o
k_etc = 0.3  # o
k_xrp = 0.5  # o
k_ada = 0.5  # o
k_eos = 0.3  # o
k_xlm = 0.1  # o
k_hbar = 0.1 # o
k_trx = 0.3  # o
k_bch = 0.5 # o

## __min_val__ ##

doge_min = 7.7
eth_min = 0.001
etc_min = 0.043
xrp_min = 2.92
ada_min = 2.16
eos_min = 0.37
xlm_min = 5.9
hbar_min = 11.6
trx_min = 32.46
bch_min = 0.00308

## trade_time_set ##

trade_minute1 = "minute1"
trade_minute60 = "minute60"
trade_minute40 = "minute240"


## function ##

def get_target_price(ticker, k):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
    # 시가 + 변동폭


# def get_ma20(ticker):
#     """20시간 이동 평균선 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
#     ma20 = df['close'].rolling(20).mean().iloc[-1]
#     return ma20

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


## 로그인 ##

upbit = pyupbit.Upbit(access, secret)

print("autotrade start")


# 자동매매 시작

while True:

    doge_val = coin_autotrade(krw_doge,k_doge,doge,doge_min,doge_val)

    eth_val = coin_autotrade(krw_eth,k_eth,eth,eth_min,eth_val)

    etc_val = coin_autotrade(krw_etc,k_etc,etc,etc_min,etc_val)

    xrp_val = coin_autotrade(krw_xrp,k_xrp,xrp,xrp_min,xrp_val)

    ada_val = coin_autotrade(krw_ada,k_ada,ada,ada_min,ada_val)

    eos_val = coin_autotrade(krw_eos,k_eos,eos,eos_min,eos_val)

    xlm_val = coin_autotrade(krw_xlm,k_xlm,xlm,xlm_min,xlm_val)

    hbar_val = coin_autotrade(krw_hbar,k_hbar,hbar,hbar_min,hbar_val)
    
    bch_val = coin_autotrade(krw_bch,k_bch,bch,bch_min,bch_val)
