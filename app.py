from flask import Flask, render_template, jsonify
import threading
import time
import os
import random

app = Flask(__name__)

state = {
    "balance": 1000000,
    "risk": 1,
    "equity": 1000000,
    "positions": [],
    "pnl": 0,
    "running": True
}

def bot_loop():
    while True:
        try:
            time.sleep(3)
            change = random.uniform(-100, 150)
            state["balance"] += change
            state["pnl"] += change
        except Exception as e:
            print("BOT ERROR:", e)

threading.Thread(target=bot_loop, daemon=True).start()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/status")
def status():
    return jsonify(state)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)