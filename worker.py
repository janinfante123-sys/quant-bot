import time
from datetime import datetime

from engine.data_feed import get_price
from engine.strategy import get_signal


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
# 🔥 CLASIFICACIÓN DE ACTIVOS
# ==========================
def get_asset_type(symbol):
    if "-USD" in symbol:
        return "CRYPTO"
    return "STOCK"


def run(state):
    print("🟢 BOT LOOP STARTED")

    while True:
        start = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.utcnow().strftime('%H:%M:%S')}")

        for symbol in SYMBOLS:
            try:
                df, price = get_price(symbol, interval="1h")
                signal, regime = get_signal(df)

                print(f"{symbol} → {price} → {signal} → {regime}")

                # ==========================
                # SL / TP AUTOMÁTICO
                # ==========================
                state.check_positions(symbol, price)

                # ==========================
                # 🔥 FILTRO DE CORRELACIÓN
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
                        state.open_position(symbol, price, side="BUY")

                elif signal == "SELL":

                    if asset_type in open_types:
                        print(f"⛔ SKIP {symbol} (correlated)")
                    else:
                        state.open_position(symbol, price, side="SELL")

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {round(state.balance, 2)}")

        duration = round(time.time() - start, 2)
        print(f"⏱ {duration}s")
        print("⏳ sleeping...")

        time.sleep(LOOP_INTERVAL)