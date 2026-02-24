from flask import Flask, render_template, jsonify
import threading
import time
import os
import yfinance as yf
import random

app = Flask(__name__)

# ===== CAPITAL =====
state = {
    "balance": 1_000_000,
    "equity": 1_000_000,
    "risk": 0.01,
    "positions": {},
    "trades": [],
    "running": True
}

# ===== MERCADOS =====
symbols = ["BTC-USD","ETH-USD","EURUSD=X","SPY","AAPL"]

# ===== DATOS =====
def get_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(df) > 0:
            return float(df["Close"].iloc[-1])
    except:
        return None

# ===== ABRIR TRADE =====
def open_trade(symbol, price):
    risk_amount = state["equity"] * state["risk"]
    size = risk_amount / price

    stop = price * 0.99
    tp = price * 1.02

    state["positions"][symbol] = {
        "entry": price,
        "size": size,
        "stop": stop,
        "tp": tp
    }

# ===== CERRAR TRADE =====
def close_trade(symbol, price):
    pos = state["positions"][symbol]
    pnl = (price - pos["entry"]) * pos["size"]

    state["balance"] += pnl
    state["equity"] = state["balance"]

    state["trades"].append({
        "symbol": symbol,
        "entry": pos["entry"],
        "exit": price,
        "pnl": pnl
    })

    del state["positions"][symbol]

# ===== BOT LOOP =====
def bot_loop():
    while True:
        try:
            for s in symbols:
                price = get_price(s)
                if price is None:
                    continue

                # abrir trade si no hay
                if s not in state["positions"]:
                    if random.random() < 0.05:
                        open_trade(s, price)

                # gestionar trade
                if s in state["positions"]:
                    pos = state["positions"][s]

                    if price <= pos["stop"]:
                        close_trade(s, price)

                    elif price >= pos["tp"]:
                        close_trade(s, price)

            time.sleep(20)

        except Exception as e:
            print("BOT ERROR:", e)
            time.sleep(5)

threading.Thread(target=bot_loop, daemon=True).start()

# ===== WEB =====
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/status")
def status():
    return jsonify(state)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)