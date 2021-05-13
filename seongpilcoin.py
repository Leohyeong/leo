import pyupbit
import numpy as np
import time
from datetime import date, datetime, timedelta

## Initial ##


doge = "KRW-DOGE"
eth = "KRW-ETH"
etc = "KRW-ETC"
xrp = "KRW-XRP"
ada = "KRW-ADA"
eos = "KRW-EOS"

k_doge = 0.1
k_eth = 0.6
k_etc = 0.5
k_xrp = 0.2
k_ada = 0.6
k_eos = 0.1


trade_hours60 = "minute60"
trade_hours240 = "minute240"
hour_counts = 48

## Balance ##

access = "OFCL17jSpSEAj3r1gnvHAGPMSix5MShrAcsz9Hi4"
secret = "04fFGc0jmnpOupg3T2DfejiFGuojYiMFVwIPGiXU"

upbit = pyupbit.Upbit(access,secret)

## date ##

start_day = datetime(2021,5,10)
# start_day = datetime(2021,2,20)
today = datetime.now()
days = (today-start_day).days



###########        DOGE        ############

def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(doge,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))


k = 0.5

df = pyupbit.get_ohlcv(doge,interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_doge
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), doge)
df.to_excel("loss.xlsx")

print(df)

# ###########        ETH        ############

def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(eth,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))

df = pyupbit.get_ohlcv(eth, interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_eth
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), eth)
df.to_excel("loss.xlsx")

print(df)

###########        ETC        ############

def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(etc,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))


k = 0.2

df = pyupbit.get_ohlcv(etc, interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_etc
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), etc)
df.to_excel("loss.xlsx")

print(df)

###########        XRP        ############


def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(xrp,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))

df = pyupbit.get_ohlcv(xrp, interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_xrp
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), xrp)
df.to_excel("loss.xlsx")

print(df)

###########        ADA        ############


def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(ada,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))

df = pyupbit.get_ohlcv(ada, interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_ada
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), ada)
df.to_excel("loss.xlsx")

print(df)

###########        EOS        ############


def get_ror(kt=0.5):
    df = pyupbit.get_ohlcv(eos,interval=trade_hours60, count = hour_counts)
    df['range'] = (df['high'] - df['low']) * kt
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

for kt in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(kt)
    print("%.1f %f" % (kt, ror))

df = pyupbit.get_ohlcv(eos, interval=trade_hours60, count = hour_counts)
df['range'] = (df['high'] - df['low']) * k_eos
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

df['ror_tempt'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
df['hpr_tempt'] = df['ror_tempt'].cumprod() # 누적수익률

df['ror'] = 100 * (np.where(df['high'] > df['target'], # 수익률 // (조건문, 참일때 값, 거짓일때 값)
                     df['close'] / df['target'] - fee,
                     1) - 1)
df['hpr'] = 100 * (df['ror_tempt'].cumprod() - 1) # 누적수익률

df['loss'] = (df['hpr_tempt'].cummax() - df['hpr_tempt']) / df['hpr_tempt'].cummax() * 100 # (누적최대값과 현재 hpr / 누적 최대값 * 100)

print("MDD(%): ", df['loss'].max(), eos)
df.to_excel("loss.xlsx")

print(df)
