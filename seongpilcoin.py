import time
import pyupbit
import datetime

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"

k_doge = 0.1
k_eth = 0.6
k_etc = 0.5
k_xrp = 0.2

XRP_balance = "XRP"
XRPcoin = "KRW-XRP"

ETH_balance = "ETH"
ETHcoin = "KRW-ETH"

DOGE_balance = "DOGE"
DOGEcoin = "KRW-DOGE"

ETC_balance = "ETC"
ETCcoin = "KRW-ETC"

def get_target_price(ticker, k):
    """변동성 돌파 전략 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
    # 시가 + 변동폭


def get_ma20(ticker):
    """20시간 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=1)
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

# 로그인
upbit = pyupbit.Upbit(access, secret)

print("autotrade start")


# 자동매매 시작
while True:

################################## XRP ##################################

    try:
        now = datetime.datetime.now()
        start_time = get_start_time(XRPcoin)
        end_time = start_time + datetime.timedelta(hours=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(XRPcoin, k_xrp)
            ma20 = get_ma20(XRPcoin)
            current_price = get_current_price(XRPcoin)
            if ma20 < target_price < current_price:
                krw = get_balance("KRW")
                xrp = get_balance(XRP_balance)
                if krw > 5000 and xrp < 2.7:
                    upbit.buy_market_order(XRPcoin, 50000)
                    print("BUY XRP COIN")
        else:
            xrp = get_balance(XRP_balance)
            if xrp > 2.7:
                upbit.sell_market_order(XRPcoin, xrp)
                print("SELL XRP COIN")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

################################## ETH ##################################

    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ETHcoin)
        end_time = start_time + datetime.timedelta(hours=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(ETHcoin, k_eth)
            ma20 = get_ma20(ETHcoin)
            current_price = get_current_price(ETHcoin)
            if ma20 < target_price < current_price:
                krw = get_balance("KRW")
                eth = get_balance(ETH_balance)
                if krw > 5000 and eth < 0.0009:
                    upbit.buy_market_order(ETHcoin, 50000)
                    print("BUY ETH COIN")
        else:
            eth = get_balance(ETH_balance)
            if eth > 0.0009:
                upbit.sell_market_order(ETHcoin, eth)
                print("SELL ETH COIN")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
    
################################## DOGE ##################################

    try:
        now = datetime.datetime.now()
        start_time = get_start_time(DOGEcoin)
        end_time = start_time + datetime.timedelta(hours=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(DOGEcoin, k_doge)
            ma20 = get_ma20(DOGEcoin)
            current_price = get_current_price(DOGEcoin)
            if ma20 < target_price < current_price:
                krw = get_balance("KRW")
                doge = get_balance(DOGE_balance)
                if krw > 5000 and doge < 8.2:
                    upbit.buy_market_order(DOGEcoin, 50000)
                    print("BUY DOGE COIN")
        else:
            doge = get_balance(DOGE_balance)
            if doge > 8.2:
                upbit.sell_market_order(DOGEcoin, doge)
                print("SELL DOGE COIN")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

################################## ETC ##################################

    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ETCcoin)
        end_time = start_time + datetime.timedelta(hours=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(ETCcoin, k_etc)
            ma20 = get_ma20(ETCcoin)
            current_price = get_current_price(ETCcoin)
            if ma20 < target_price < current_price:
                krw = get_balance("KRW")
                etc = get_balance(ETC_balance)
                if krw > 5000 and etc < 0.036:
                    upbit.buy_market_order(ETCcoin, 50000)
                    print("BUY ETC COIN")
        else:
            etc = get_balance(ETC_balance)
            if etc > 0.036:
                upbit.sell_market_order(ETCcoin, etc)
                print("SELL ETC COIN")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
