def generate_signal(df):
    df = df.copy()

    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    if df["ema20"].iloc[-2] < df["ema50"].iloc[-2] and df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:
        return "BUY"

    if df["ema20"].iloc[-2] > df["ema50"].iloc[-2] and df["ema20"].iloc[-1] < df["ema50"].iloc[-1]:
        return "SELL"

    return "HOLD"