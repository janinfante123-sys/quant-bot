import pandas as pd


def get_signal(df):

    try:

        if df is None or df.empty:
            return "HOLD"

        close = df["Close"]

        if len(close) < 50:
            return "HOLD"

        # ======================
        # INDICADORES
        # ======================

        sma20 = close.rolling(20).mean()

        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        price = float(close.iloc[-1])
        sma = float(sma20.iloc[-1])
        rsi_val = float(rsi.iloc[-1])

        if pd.isna(sma) or pd.isna(rsi_val):
            return "HOLD"

        # ======================
        # TREND STRATEGY
        # ======================

        if price > sma and rsi_val < 50:
            return "BUY"

        if price < sma and rsi_val > 50:
            return "SELL"

        # ======================
        # MEAN REVERSION
        # ======================

        if rsi_val < 30:
            return "BUY"

        if rsi_val > 70:
            return "SELL"

        return "HOLD"

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD"