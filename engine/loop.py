import time
from datetime import datetime
from config import SYMBOLS, LOOP_INTERVAL, RISK_PER_TRADE
from engine.data_feed import get_price
from engine.strategy import generate_signal
from engine.risk import position_size
from engine.executor import open_trade, check_closures

def run(state):
    print("🟢 BOT LOOP STARTED", flush=True)

    while True:
        start = time.time()

        try:
            now = datetime.utcnow().strftime("%H:%M:%S")
            print(f"\n🔁 NEW CYCLE {now}", flush=True)

            price_map = {}

            for market, symbol in SYMBOLS:
                df, price = get_price(market, symbol)
                price_map[symbol] = price

                signal = generate_signal(df)

                print(f"{symbol} → {price} → {signal}", flush=True)

                if signal != "HOLD" and len(state.open_trades) < 3:
                    atr = (df["High"] - df["Low"]).rolling(14).mean().iloc[-1]

                    if signal == "BUY":
                        sl = price - atr
                        tp = price + atr*2
                    else:
                        sl = price + atr
                        tp = price - atr*2

                    size = position_size(state.balance, RISK_PER_TRADE, price, sl)

                    open_trade(state, symbol, signal, price, sl, tp, size)

            check_closures(state, price_map)

            print(f"Balance: {round(state.balance,2)}", flush=True)

            duration = round(time.time() - start, 2)
            print(f"⏱ {duration}s", flush=True)
            print("⏳ sleeping...\n", flush=True)

            state.save()
            time.sleep(LOOP_INTERVAL)

        except Exception as e:
            print("❌ LOOP ERROR:", e, flush=True)
            time.sleep(5)