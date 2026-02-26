import yfinance as yf
import pandas as pd


def get_price(symbol, interval="1h"):
    df = yf.download(
        symbol,
        period="7d",
        interval=interval,
        progress=False,
        auto_adjust=True
    )

    if df is None or df.empty:
        raise Exception("No data received")

    # 🔥 APLANA columnas si vienen como MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if "Close" not in df.columns:
        raise Exception("Close column not found")

    # 🔥 Forzamos escalar real
    price = df["Close"].values[-1]

    return df, float(price)
