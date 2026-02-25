
import ccxt
import yfinance as yf
import pandas as pd

exchange = ccxt.binance()

def get_crypto(symbol):
    ohlc = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
    df = pd.DataFrame(ohlc, columns=['timestamp','open','high','low','close','volume'])
    return df

def get_stock(symbol):
    df = yf.download(symbol, interval="1h", period="1mo")
    df = df.rename(columns=str.lower)
    return df

def get_forex(symbol):
    df = yf.download(symbol+"=X", interval="1h", period="1mo")
    df = df.rename(columns=str.lower)
    return df
