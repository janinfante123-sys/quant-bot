import pandas as pd


def get_signal(df):
    try:
        if df is None or df.empty:
            return "HOLD"

        close = df["Close"]

        if len(close) < 50:
            return "HOLD"

        # ==========================
        # INDICADORES
        # ==========================

        sma_fast = close.rolling(10).mean()
        sma_slow = close.rolling(30).mean()

        momentum = close.pct_change(5)

        fast = sma_fast.iloc[-1]
        slow = sma_slow.iloc[-1]
        mom = momentum.iloc[-1]

        if pd.isna(fast) or pd.isna(slow) or pd.isna(mom):
            return "HOLD"

        # ==========================
        # LÓGICA
        # ==========================

        # Tendencia + momentum
        if fast > slow and mom > 0:
            return "BUY"

        elif fast < slow and mom < 0:
            return "SELL"

        else:
            return "HOLD"

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD"