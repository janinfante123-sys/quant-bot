import pandas as pd

def get_signal(df):
    try:
        if df is None or df.empty:
            return "HOLD"

        close = df["Close"]

        if len(close) < 30:
            return "HOLD"

        sma_fast = close.rolling(5).mean()
        sma_slow = close.rolling(20).mean()

        fast = float(sma_fast.iloc[-1])
        slow = float(sma_slow.iloc[-1])

        if pd.isna(fast) or pd.isna(slow):
            return "HOLD"

        if fast > slow:
            return "BUY"
        elif fast < slow:
            return "SELL"
        else:
            return "HOLD"

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD"
