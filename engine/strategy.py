import pandas as pd
import ta

class Strategy:

    def signal(self, df):

        df["ema50"] = df["close"].ewm(span=50).mean()
        df["ema200"] = df["close"].ewm(span=200).mean()
        df["rsi"] = ta.momentum.RSIIndicator(df["close"],14).rsi()
        df["atr"] = ta.volatility.AverageTrueRange(
            df["high"],df["low"],df["close"],14).average_true_range()

        last = df.iloc[-1]

        if last["ema50"] > last["ema200"] and last["rsi"] < 65:
            return "LONG", last["atr"]

        if last["ema50"] < last["ema200"] and last["rsi"] > 35:
            return "SHORT", last["atr"]

        return None, None
