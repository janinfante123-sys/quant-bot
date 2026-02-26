import yfinance as yf

def get_price(symbol):
    df = yf.download(
        symbol,
        period="7d",
        interval="1h",
        progress=False
    )

    if df is None or len(df) == 0:
        raise Exception("No data")

    price = df["Close"].iloc[-1]

    if hasattr(price, "iloc"):
        price = price.iloc[-1]

    return float(price), df
