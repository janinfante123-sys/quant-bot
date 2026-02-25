import yfinance as yf
import pandas as pd

def get_price(market, symbol):
    if market == "crypto":
        ticker = yf.Ticker(symbol.replace("/", "-"))
    elif market == "stock":
        ticker = yf.Ticker(symbol)
    else:
        ticker = yf.Ticker(symbol)

    df = ticker.history(period="1d", interval="1h")

    if df.empty:
        raise Exception("No data received")

    price = df["Close"].iloc[-1]

    return df, price
