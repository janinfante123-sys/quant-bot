import yfinance as yf

SYMBOLS = {
    "crypto": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"],
    "forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X"],
    "stocks": ["AAPL", "MSFT", "NVDA", "SPY"],
}

ALL_SYMBOLS = sum(SYMBOLS.values(), [])

def get_latest_candle(symbol: str):
    try:
        df = yf.download(
            symbol,
            period="1d",
            interval="1m",
            progress=False,
            auto_adjust=False,
        )

        if df.empty:
            return None

        last = df.iloc[-1]

        return {
            "time": str(df.index[-1]),
            "open": float(last["Open"]),
            "high": float(last["High"]),
            "low": float(last["Low"]),
            "close": float(last["Close"]),
            "volume": float(last["Volume"]),
        }

    except Exception as e:
        print(f"Data error {symbol}: {e}")
        return None
