import yfinance as yf

def get_price(market, symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="3d", interval="15m")

    if df.empty:
        raise Exception("No data received")

    price = df["Close"].iloc[-1]
    return df, price
