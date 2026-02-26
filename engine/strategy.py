import pandas as pd

def get_signal(df):
    """
    Estrategia simple:
    - BUY si cierre > MA20
    - SELL si cierre < MA20
    - HOLD en otro caso
    """

    if df is None or len(df) < 21:
        return "HOLD"

    close = df["Close"]
    ma20 = close.rolling(20).mean()

    last_close = close.iloc[-1]
    last_ma = ma20.iloc[-1]

    if pd.isna(last_ma):
        return "HOLD"

    if last_close > last_ma:
        return "BUY"
    elif last_close < last_ma:
        return "SELL"
    else:
        return "HOLD"
