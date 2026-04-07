import pandas as pd


def get_signal(df):
    try:
        if df is None or df.empty:
            return "HOLD", "UNKNOWN"

        close = df["Close"]

        if len(close) < 50:
            return "HOLD", "UNKNOWN"

        # ==========================
        # MEDIAS
        # ==========================
        sma_fast = close.rolling(10).mean()
        sma_slow = close.rolling(30).mean()

        fast = float(sma_fast.iloc[-1])
        slow = float(sma_slow.iloc[-1])

        # ==========================
        # MOMENTUM
        # ==========================
        momentum = close.iloc[-1] - close.iloc[-5]

        # ==========================
        # ATR (volatilidad)
        # ==========================
        atr = df["ATR"].iloc[-1] if "ATR" in df else 0

        # ==========================
        # REGIME DETECTION
        # ==========================
        if abs(fast - slow) / slow < 0.002:
            regime = "RANGE"
        else:
            regime = "TREND"

        # ==========================
        # SIGNAL
        # ==========================
        if regime == "TREND":

            if fast > slow and momentum > 0:
                return "BUY", regime

            elif fast < slow and momentum < 0:
                return "SELL", regime

        else:  # RANGE

            if momentum > 0:
                return "BUY", regime
            elif momentum < 0:
                return "SELL", regime

        return "HOLD", regime

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD", "UNKNOWN"