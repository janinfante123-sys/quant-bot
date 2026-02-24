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

        end = datetime.utcnow()
        start = end - timedelta(days=self.lookback_days)

        df = yf.download(
            self.symbol,
            start=start,
            end=end,
            interval=self.interval,
            progress=False,
            auto_adjust=True
        )

        if df is None or df.empty:
            print("No data downloaded")
            return pd.DataFrame()

        # 🔥 FIX CRÍTICO
        for col in ["Open","High","Low","Close","Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].astype(float)

        df = df.dropna()

        return df