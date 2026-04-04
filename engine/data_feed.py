import yfinance as yf
import pandas as pd


def get_price(symbol, interval="1h"):

    df = yf.download(
        symbol,
        period="14d",
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

    # ==========================
    # ATR (Average True Range)
    # ==========================

    if "High" in df.columns and "Low" in df.columns:

        df["H-L"] = df["High"] - df["Low"]
        df["H-C"] = abs(df["High"] - df["Close"].shift())
        df["L-C"] = abs(df["Low"] - df["Close"].shift())

        df["TR"] = df[["H-L", "H-C", "L-C"]].max(axis=1)

        df["ATR"] = df["TR"].rolling(14).mean()

    else:
        df["ATR"] = 0

    # 🔥 Forzamos escalar real
    price = df["Close"].values[-1]

    return df, float(price)