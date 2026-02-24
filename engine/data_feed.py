import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataFeed:

    def __init__(self, symbol="BTC-USD", interval="1h", lookback_days=30):
        self.symbol = symbol
        self.interval = interval
        self.lookback_days = lookback_days

    def get_data(self):
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=self.lookback_days)

        df = yf.download(
            self.symbol,
            start=start_date,
            end=end_date,
            interval=self.interval,
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            raise ValueError("No market data returned")

        # 🔥 FIX IMPORTANTE: asegurar arrays 1D
        df["Close"] = np.array(df["Close"]).flatten()
        df["Open"] = np.array(df["Open"]).flatten()
        df["High"] = np.array(df["High"]).flatten()
        df["Low"] = np.array(df["Low"]).flatten()
        df["Volume"] = np.array(df["Volume"]).flatten()

        df = df.dropna()

        return df