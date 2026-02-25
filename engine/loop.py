import time
from datetime import datetime
from config import SYMBOLS, LOOP_INTERVAL
from engine.data_feed import get_price

def run(state):
    print("🟢 BOT LOOP STARTED", flush=True)

    while True:
        start = time.time()

        try:
            now = datetime.utcnow().strftime("%H:%M:%S")
            print(f"\n🔁 NEW CYCLE {now}", flush=True)

            for market, symbol in SYMBOLS:
                df, price = get_price(market, symbol)
                print(f"{symbol} → {round(price,2)}", flush=True)

            duration = round(time.time() - start, 2)
            print(f"⏱ cycle duration: {duration}s", flush=True)
            print("⏳ sleeping...\n", flush=True)

            time.sleep(LOOP_INTERVAL)

        except Exception as e:
            print("❌ LOOP ERROR:", e, flush=True)
            time.sleep(5)
