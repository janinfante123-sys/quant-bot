
def generate_signal(df):
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()

    if df['ema20'].iloc[-1] > df['ema50'].iloc[-1]:
        return "BUY"
    elif df['ema20'].iloc[-1] < df['ema50'].iloc[-1]:
        return "SELL"
    return "HOLD"
