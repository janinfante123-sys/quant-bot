import pandas as pd


def detect_market_regime(df):
    try:
        if df is None or df.empty:
            return "UNKNOWN"

        close = df["Close"]

        if len(close) < 50:
            return "UNKNOWN"

        # Volatilidad
        returns = close.pct_change()
        vol = returns.rolling(20).std().iloc[-1]

        # Tendencia
        sma_fast = close.rolling(10).mean().iloc[-1]
        sma_slow = close.rolling(30).mean().iloc[-1]

        # Fuerza tendencia
        trend_strength = abs(sma_fast - sma_slow) / close.iloc[-1]

        # ==========================
        # CLASIFICACIÓN
        # ==========================

        if trend_strength > 0.01 and vol > 0.002:
            return "TREND"

        return "RANGE"

    except Exception as e:
        print("⚠️ AI MODULE ERROR:", e)
        return "UNKNOWN"