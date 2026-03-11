import pandas as pd

def get_signal(df):
    try:
        if df is None or df.empty:
            return "HOLD"

        close = df["Close"]

        # necesitamos suficientes datos
        if len(close) < 210:
            return "HOLD"

        sma_fast = close.rolling(5).mean()
        sma_slow = close.rolling(20).mean()
        sma_trend = close.rolling(200).mean()

        fast = float(sma_fast.iloc[-1])
        slow = float(sma_slow.iloc[-1])
        trend = float(sma_trend.iloc[-1])
        price = float(close.iloc[-1])

        if pd.isna(fast) or pd.isna(slow) or pd.isna(trend):
            return "HOLD"

        signal = "HOLD"

        # señal base
        if fast > slow:
            signal = "BUY"
        elif fast < slow:
            signal = "SELL"

        # filtro de tendencia
        if price > trend:
            market_trend = "BULL"
        else:
            market_trend = "BEAR"

        if signal == "BUY" and market_trend != "BULL":
            return "HOLD"

        if signal == "SELL" and market_trend != "BEAR":
            return "HOLD"

        return signal

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD"