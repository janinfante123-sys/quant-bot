import time
from datetime import datetime

from engine.data_feed import get_price
from engine.strategy import get_signal
from engine.state import BotState

SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "AAPL"]
SLEEP = 900  # 15 minutos

def run():
    state = BotState()

    print("🚀 WORKER STARTED")
    print("🟢 BOT LOOP STARTED")

    while True:
        start = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.now().strftime('%H:%M:%S')}")

        for symbol in SYMBOLS:
            try:
                price, df = get_price(symbol)
                signal = get_signal(df)

                print(f"{symbol} → {price} → {signal}")

                state.process_signal(symbol, signal, price)

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {round(state.balance,2)}")
        print(f"⏱ {round(time.time()-start,2)}s")
        print("⏳ sleeping...\n")

        time.sleep(SLEEP)
