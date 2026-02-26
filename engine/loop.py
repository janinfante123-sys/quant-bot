import time
from datetime import datetime

from config import SYMBOLS, LOOP_INTERVAL, START_BALANCE, RISK_PER_TRADE
from engine.data_feed import get_data


balance = START_BALANCE
positions = {}


def simple_signal(df):
    """
    Señal básica:
    - Compra si cierre actual > media 20
    - Vende si cierre actual < media 20
    """
    close = df["Close"]
    ma20 = close.rolling(20).mean()

    if len(ma20) < 21:
        return "HOLD"

    if close.iloc[-1] > ma20.iloc[-1]:
        return "BUY"
    elif close.iloc[-1] < ma20.iloc[-1]:
        return "SELL"
    else:
        return "HOLD"


def run():
    global balance
    global positions

    print("🟢 BOT LOOP STARTED")

    while True:
        start_time = time.time()
        print(f"\n🔁 NEW CYCLE {datetime.now().strftime('%H:%M:%S')}")

        for symbol in SYMBOLS:
            try:
                df = get_data(symbol)
                price = float(df["Close"].iloc[-1])
                signal = simple_signal(df)

                print(f"{symbol} → {price} → {signal}")

                # Abrir posición
                if signal == "BUY" and symbol not in positions:
                    size = balance * RISK_PER_TRADE
                    positions[symbol] = {
                        "entry": price,
                        "size": size
                    }
                    balance -= size
                    print(f"OPEN {symbol}")

                # Cerrar posición
                elif signal == "SELL" and symbol in positions:
                    entry = positions[symbol]["entry"]
                    size = positions[symbol]["size"]
                    pnl = size * (price / entry)
                    balance += pnl
                    del positions[symbol]
                    print(f"CLOSE {symbol}")

            except Exception as e:
                print(f"❌ ERROR {symbol}: {e}")

        print(f"Balance: {round(balance, 2)}")

        duration = round(time.time() - start_time, 2)
        print(f"⏱ {duration}s")
        print("⏳ sleeping...\n")

        time.sleep(LOOP_INTERVAL)