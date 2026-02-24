import yfinance as yf
import requests
import pandas as pd

def get_crypto(symbol):
    r = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=300")
    data = r.json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","vol","a","b","c","d","e","f"
    ])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    return df

def get_stock(symbol):
    df = yf.download(symbol, interval="1h", period="60d")
    df = df.rename(columns={"Close":"close","High":"high","Low":"low"})
    return df

def get_all_data():
    return {
        "BTCUSDT": get_crypto("BTCUSDT"),
        "ETHUSDT": get_crypto("ETHUSDT"),
        "AAPL": get_stock("AAPL"),
        "MSFT": get_stock("MSFT"),
        "SPY": get_stock("SPY"),
    }
