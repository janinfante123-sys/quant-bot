import time
from datetime import datetime

from engine.data_feed import get_price
from engine.strategy import get_signal
from engine.ai_module import detect_market_regime


SYMBOLS = [
    # CRYPTO
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",

    # STOCKS
    "AAPL",
    "MSFT",
    "NVDA",
    "SPY"
]

LOOP_INTERVAL = 3600


def run(state):
    print("🟢 BOT LOOP STARTED")

    while True:
        start = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.utcnow().strftime('%H:%M:%S')}")

        state.update_cooldowns()

        for symbol in SYMBOLS:
            try:
                df, price = get_price(symbol, interval="1h")

                regime = detect_market_regime(df)
                signal = str(get_signal(df))

                print(f"{symbol} → {price} → {signal} → {regime}")

                # ==========================
                # CHECK SL / TP
                # ==========================
                state.check_positions(symbol, price)

                # ==========================
                # FILTRO IA (CLAVE)
                # ==========================
                if regime != "TREND":
                    continue

                # ==========================
                # EJECUCIÓN
                # ==========================
                if signal == "BUY":
                    state.open_position(symbol, price, side="BUY")

                elif signal == "SELL":
                    state.open_position(symbol, price, side="SELL")

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {round(state.balance, 2)}")

        duration = round(time.time() - start, 2)
        print(f"⏱ {duration}s")
        print("⏳ sleeping...")

        time.sleep(LOOP_INTERVAL)