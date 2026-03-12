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

        sma = close.rolling(20).mean()

        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        price = float(close.iloc[-1])
        sma_val = float(sma.iloc[-1])
        rsi_val = float(rsi.iloc[-1])

        if pd.isna(sma_val) or pd.isna(rsi_val):
            return "HOLD"

        # ======================
        # LÓGICA DE TRADING
        # ======================

        # LONG
        if price > sma_val and rsi_val < 40:
            return "BUY"

        # SHORT
        if price < sma_val and rsi_val > 60:
            return "SELL"

        return "HOLD"

    except Exception as e:
        print("⚠️ STRATEGY ERROR:", e)
        return "HOLD"