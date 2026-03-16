import json
import os
from datetime import datetime


class Metrics:

    FILE = "metrics.json"

    def __init__(self):
        self.trades = []
        self._load()

    def _save(self):
        data = {
            "trades": self.trades
        }
        with open(self.FILE, "w") as f:
            json.dump(data, f, indent=4)

    def _load(self):
        if os.path.exists(self.FILE):
            with open(self.FILE, "r") as f:
                data = json.load(f)
                self.trades = data.get("trades", [])
                print("📊 METRICS RESTORED")

    def record_trade(self, symbol, entry, exit_price, size, pnl):

        trade = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "entry": entry,
            "exit": exit_price,
            "size": size,
            "pnl": pnl
        }

        self.trades.append(trade)
        self._save()

    def summary(self):

        total = len(self.trades)
        if total == 0:
            return {}

        wins = [t for t in self.trades if t["pnl"] > 0]
        losses = [t for t in self.trades if t["pnl"] <= 0]

        gross_profit = sum(t["pnl"] for t in wins)
        gross_loss = abs(sum(t["pnl"] for t in losses))

        winrate = len(wins) / total * 100
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0

        equity = 0
        peak = 0
        max_dd = 0

        for t in self.trades:
            equity += t["pnl"]
            peak = max(peak, equity)
            dd = peak - equity
            max_dd = max(max_dd, dd)

        return {
            "total_trades": total,
            "winrate": round(winrate, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(max_dd, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2)
        }
