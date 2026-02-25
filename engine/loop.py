import time
from engine.data_feed import ALL_SYMBOLS, get_latest_candle
from engine.state import state

RUNNING = False

def process_symbol(symbol):
    candle = get_latest_candle(symbol)
    if not candle:
        return

    last_time = state.last_candle_time.get(symbol)
    if last_time == candle["time"]:
        return

    state.last_candle_time[symbol] = candle["time"]

    print(
        f"[{symbol}] "
        f"{candle['time']} | "
        f"O:{candle['open']} "
        f"H:{candle['high']} "
        f"L:{candle['low']} "
        f"C:{candle['close']}"
    )

def run_loop():
    global RUNNING
    RUNNING = True

    print("=== ENGINE LOOP STARTED ===")

    while RUNNING:
        try:
            for symbol in ALL_SYMBOLS:
                process_symbol(symbol)

            time.sleep(5)

        except Exception as e:
            print("Loop error:", e)
            time.sleep(5)
