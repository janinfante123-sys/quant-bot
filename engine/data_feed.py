import yfinance as yf

TIMEFRAME = "1h"
LIMIT = 200

def get_price(symbol):
    try:
        df = yf.download(
            symbol,
            period="7d",
            interval=TIMEFRAME,
            progress=False
        )

        if df is None or len(df) == 0:
            raise Exception("No data")

        close = df["Close"].iloc[-1]

        # 🔥 FIX DEFINITIVO
        if hasattr(close, "iloc"):
            close = close.iloc[-1]

        return float(close), df

    except Exception as e:
        raise Exception(f"No data received for {symbol}: {e}")