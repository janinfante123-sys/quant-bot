from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# Estado global del bot
bot_data = {
    "balance": 1000000,
    "risk": 0.01,
    "positions": [],
    "equity_curve": []
}

# -------------------------
# BOT SIMULADO (paper trading)
# -------------------------
def run_bot():
    while True:
        # simulación simple para comprobar que funciona
        bot_data["balance"] += 1
        bot_data["equity_curve"].append(bot_data["balance"])
        time.sleep(5)

# Iniciar bot en segundo plano
threading.Thread(target=run_bot, daemon=True).start()

# -------------------------
# WEB
# -------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/status")
def status():
    return jsonify(bot_data)

# IMPORTANTE PARA RENDER
if __name__ == "__main__":
    app.run()