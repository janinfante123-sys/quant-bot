import yfinance as yf

def get_price(symbol, interval="1h"):
    df = yf.download(
        symbol,
        period="7d",
        interval=interval,
        progress=False
    )

    if df is None or df.empty:
        raise Exception("No data received")

    price = float(df["Close"].iloc[-1])

    return df, price
