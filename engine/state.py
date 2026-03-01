import json
import os


class BotState:

    FILE = "bot_state.json"
    MAX_POSITIONS = 2

    def __init__(self):
        self.balance = 1000
        self.positions = {}
        self._load()

    # ==========================
    # PERSISTENCIA
    # ==========================

    def _save(self):
        data = {
            "balance": self.balance,
            "positions": self.positions
        }
        with open(self.FILE, "w") as f:
            json.dump(data, f)

    def _load(self):
        if os.path.exists(self.FILE):
            with open(self.FILE, "r") as f:
                data = json.load(f)
                self.balance = data.get("balance", 1000)
                self.positions = data.get("positions", {})
                print("🔄 STATE RESTORED")

    # ==========================
    # RIESGO 1%
    # ==========================

    def _calc_size(self, entry, sl):
        risk_amount = self.balance * 0.01
        risk_per_unit = abs(entry - sl)

        if risk_per_unit == 0:
            return 0

        return risk_amount / risk_per_unit

    # ==========================
    # ABRIR POSICIÓN
    # ==========================

    def open_position(self, symbol, price):

        if symbol in self.positions:
            return

        # 🔒 LÍMITE DE POSICIONES
        if len(self.positions) >= self.MAX_POSITIONS:
            print("⚠️ MAX POSITIONS REACHED")
            return

        sl = price * 0.99
        tp = price * 1.02

        size = self._calc_size(price, sl)

        if size <= 0:
            return

        self.positions[symbol] = {
            "entry": price,
            "size": size,
            "sl": sl,
            "tp": tp
        }

        self._save()

        print(f"OPEN {symbol} @ {price} SL:{sl} TP:{tp}")

    # ==========================
    # CERRAR MANUAL
    # ==========================

    def close_position(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        entry = pos["entry"]
        size = pos["size"]

        pnl = size * ((price - entry) / entry)
        self.balance += pnl

        del self.positions[symbol]

        self._save()

        print(f"CLOSE {symbol} @ {price} PnL:{pnl}")

    # ==========================
    # SL / TP AUTOMÁTICO
    # ==========================

    def check_positions(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        if price <= pos["sl"]:
            pnl = pos["size"] * ((price - pos["entry"]) / pos["entry"])
            self.balance += pnl
            print(f"STOP LOSS {symbol} PnL:{pnl}")
            del self.positions[symbol]
            self._save()
            return

        if price >= pos["tp"]:
            pnl = pos["size"] * ((price - pos["entry"]) / pos["entry"])
            self.balance += pnl
            print(f"TAKE PROFIT {symbol} PnL:{pnl}")
            del self.positions[symbol]
            self._save()
            return