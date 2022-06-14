import math
import time

from binance.client import Client
import pandas as pd
import ta
import numpy as np
import pandas_ta as pta

trdPair1 = 'BTC'
trdPair2 = 'USDT'

file="credentials.txt"


with open("credentials.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    API_KEY=lines[0]
    API_SECRET=lines[1]
    client = Client(API_KEY,API_SECRET)

def getminutedata(symbol):
    df = pd.DataFrame(client.get_historical_klines(symbol, '5m', '240m UTC'))
    df = df.iloc[:, :6]
    df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
    df = df.set_index('open_time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    btclastprice = df['close'][len(df['close']) - 1]
    print("anlik btc fiyatı={}".format(btclastprice))

    return df
df= getminutedata(trdPair1 + trdPair2)

def rsi(df, periods=14, ema=True):
    close_delta = df['close'].diff()

    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    rsilastvalue= rsi[len(rsi) - 1]


    return rsilastvalue




btclastprice=df['close'][len(df['close'])-1]
a=rsi(df, periods=14, ema=True)
btcCount = client.get_asset_balance(asset = "BTC")
btcCount=float(btcCount['free'])
print("BTC MIKTARI={}".format(btcCount))
usdtCount = client.get_asset_balance(asset = "USDT")
usdtCount = float(usdtCount['free'])
print("USDT MIKTARI={}".format(usdtCount))
adet= usdtCount / btclastprice
adet=format(float(adet), '.4f')
print("Quantitiy={}".format(adet))
stat='sell'
print(rsi(df, periods=14, ema=True))
#BUYING BTC
while True:
    if stat=='sell' and a < 50 :

        stat = 'buy'
        signal='send'
        order = client.order_market_buy(symbol=trdPair1 + trdPair2, quantity=float(adet))
        print("BTC BUY")

    elif stat=='sell' and a > 50:
        print("HOLD USDT")
        with open("signal.txt",'w',encoding = 'utf-8') as f:
            f.write("BUY")
        time.sleep(2)
    #SELLING BTC



    if stat=='buy' and a > 55 :
        stat = 'sell'
        order=client.order_market_sell(symbol="BTCUSDT", quantity=float(btcCount))
        print("BTC SELL")
        time.sleep(2)
    elif stat=='buy' and a < 55 :
        print("HOLD BTC")
        time.sleep(2)