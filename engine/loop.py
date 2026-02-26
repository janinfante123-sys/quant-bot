import time
from datetime import datetime

from engine.data_feed import get_price
from engine.strategy import get_signal


SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "AAPL"
]

LOOP_INTERVAL = 3600  # 1 hora


def run(state):
    print("🟢 BOT LOOP STARTED")

    while True:
        start = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.utcnow().strftime('%H:%M:%S')}")

        for symbol in SYMBOLS:
            try:
                df, price = get_price(symbol, interval="1h")
                signal = str(get_signal(df))

                print(f"{symbol} → {price} → {signal}")

                # ===== EJECUCIÓN =====
                if signal == "BUY":
                    state.open_position(symbol, price)

                elif signal == "SELL":
                    state.close_position(symbol, price)

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {state.balance}")

        duration = round(time.time() - start, 2)
        print(f"⏱ {duration}s")
        print("⏳ sleeping...")

        time.sleep(LOOP_INTERVAL)
