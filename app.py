from flask import Flask, render_template, jsonify
import threading
import time

from engine.portfolio import Portfolio
from engine.strategy import Strategy
from engine.risk import RiskManager
from engine.data_feed import get_all_data
from engine.metrics import metrics
from engine.ai_layer import AdaptiveAI

app = Flask(__name__)

portfolio = Portfolio(1_000_000)
strategy = Strategy()
risk = RiskManager()
ai = AdaptiveAI()

def loop():
    while True:
        data = get_all_data()

        for symbol, df in data.items():

            sig, atr = strategy.signal(df)
            price = float(df.iloc[-1]["close"])

            ai.detect_regime(df)
            risk_pct = ai.adjust_risk(portfolio)

            if symbol not in portfolio.positions:
                if sig and risk.allow_trade(portfolio):
                    stop = price - atr*1.5 if sig=="LONG" else price + atr*1.5
                    portfolio.open_position(symbol, price, stop, risk_pct)

            else:
                pos = portfolio.positions[symbol]
                if price <= pos["stop"] or price >= pos["entry"] + atr*2:
                    portfolio.close_position(symbol, price)

        portfolio.update_equity()
        time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

@app.route("/")
def dash():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    return jsonify({
        "balance": portfolio.cash,
        "positions": portfolio.positions,
        "trades": portfolio.trades[-20:],
        "equity": portfolio.equity_curve,
        "metrics": metrics(portfolio),
        "ai":{
            "risk": ai.current_risk,
            "regime": ai.regime
        }
    })

if __name__ == "__main__":
    app.run()
