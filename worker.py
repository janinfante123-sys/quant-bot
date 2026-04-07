import time
from datetime import datetime, UTC

from engine.data_feed import get_price
from engine.strategy import get_signal
from engine.state import BotState


SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "AAPL",
    "MSFT",
    "NVDA",
    "SPY"
]

LOOP_INTERVAL = 3600  # 1 hora


# ==========================
# CLASIFICACIÓN ACTIVOS
# ==========================
def get_asset_type(symbol):
    if "-USD" in symbol:
        return "CRYPTO"
    return "STOCK"


def safe_start():
    try:
        state = BotState()
        run(state)
    except Exception as e:
        print("💥 FATAL ERROR ON START:", e)
        import traceback
        traceback.print_exc()
        time.sleep(60)


def run(state):
    print("🟢 BOT LOOP STARTED")

    while True:
        start = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.now(UTC).strftime('%H:%M:%S')}")

        # 🔥 actualizar cooldowns
        state.update_cooldowns()

        for symbol in SYMBOLS:
            try:
                df, price = get_price(symbol, interval="1h")
                signal, regime = get_signal(df)

                print(f"{symbol} → {price} → {signal} → {regime}")

                # ==========================
                # SL / TP CHECK
                # ==========================
                state.check_positions(symbol, price)

                # ==========================
                # ATR (🔥 NUEVO)
                # ==========================
                atr = df["ATR"].iloc[-1] if "ATR" in df else 0

                # ==========================
                # FILTRO CORRELACIÓN
                # ==========================
                asset_type = get_asset_type(symbol)

                open_types = [
                    get_asset_type(s)
                    for s in state.positions.keys()
                ]

                # ==========================
                # EJECUCIÓN
                # ==========================
                if signal == "BUY":

                    if asset_type in open_types:
                        print(f"⛔ SKIP {symbol} (correlated)")
                    else:
                        state.open_position(symbol, price, side="BUY", atr=atr)

                elif signal == "SELL":

                    if asset_type in open_types:
                        print(f"⛔ SKIP {symbol} (correlated)")
                    else:
                        state.open_position(symbol, price, side="SELL", atr=atr)

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {round(state.balance, 2)}")

        duration = round(time.time() - start, 2)
        print(f"⏱ {duration}s")
        print("⏳ sleeping...")

        time.sleep(LOOP_INTERVAL)


if __name__ == "__main__":
    print("🚀 WORKER STARTED")
    safe_start()