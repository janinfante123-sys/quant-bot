import yfinance as yf
from config import DATA_INTERVAL, DATA_LOOKBACK


def get_data(symbol):
    df = yf.download(
        symbol,
        period=DATA_LOOKBACK,
        interval=DATA_INTERVAL,
        progress=False,
        auto_adjust=True
    )

    if df is None or len(df) == 0:
        raise Exception(f"No data received for {symbol}")

    return df