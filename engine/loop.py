import time
from config import SYMBOLS, LOOP_INTERVAL
from engine.data_feed import get_price

def run(state):
    print("🟢 BOT LOOP STARTED", flush=True)

    while True:
        try:
            print("🔁 NEW CYCLE", flush=True)

            for market, symbol in SYMBOLS:
                print(f"Checking {symbol}", flush=True)
                df, price = get_price(market, symbol)

            print("⏳ sleeping...", flush=True)
            time.sleep(LOOP_INTERVAL)

        except Exception as e:
            print("❌ LOOP ERROR:", e, flush=True)
            time.sleep(5)
