from flask import Flask, render_template, jsonify
import threading
import time
import os

app = Flask(__name__)

# estado fake mientras probamos
state = {
    "balance": 1000000,
    "risk": 1,
    "positions": [],
    "running": True
}

def bot_loop():
    while True:
        time.sleep(5)
        # simulación simple
        state["balance"] += 1

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