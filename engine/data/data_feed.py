
import pandas as pd
import numpy as np

class DataFeed:

    def synthetic(self, rows=500):

        price = np.cumsum(np.random.normal(0,1,rows)) + 100

        df = pd.DataFrame({
            "close": price
        })

        df["open"] = df["close"]
        df["high"] = df["close"] + np.random.rand(rows)
        df["low"] = df["close"] - np.random.rand(rows)
        df["volume"] = np.random.rand(rows) * 1000

        return df
