import json
import os
from engine.metrics import Metrics


class BotState:

    FILE = "bot_state.json"
    MAX_POSITIONS = 2

    def __init__(self):
        self.balance = 1000
        self.positions = {}
        self.metrics = Metrics()
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

    def open_position(self, symbol, price, df, side="BUY"):

        if symbol in self.positions:
            return

        if len(self.positions) >= self.MAX_POSITIONS:
            print("⚠️ MAX POSITIONS REACHED")
            return

        # ==========================
        # ATR STOP LOSS
        # ==========================

        atr = df["ATR"].iloc[-1]

        if atr == 0 or atr is None:
            return

        if side == "BUY":
            sl = price - (2 * atr)
            tp = price + (4 * atr)
        else:
            sl = price + (2 * atr)
            tp = price - (4 * atr)

        size = self._calc_size(price, sl)

        if size <= 0:
            return

        self.positions[symbol] = {
            "entry": price,
            "size": size,
            "sl": sl,
            "tp": tp,
            "side": side
        }

        self._save()

        print(f"OPEN {side} {symbol} @ {price} SL:{sl} TP:{tp}")

    # ==========================
    # CIERRE GENERAL
    # ==========================

    def _close_and_record(self, symbol, price):

        pos = self.positions[symbol]
        entry = pos["entry"]
        size = pos["size"]
        side = pos.get("side", "BUY")

        if side == "BUY":
            pnl = size * (price - entry)
        else:
            pnl = size * (entry - price)

        self.balance += pnl

        self.metrics.record_trade(
            symbol=symbol,
            entry=entry,
            exit_price=price,
            size=size,
            pnl=pnl
        )

        del self.positions[symbol]
        self._save()

        print(f"CLOSE {symbol} @ {price} PnL:{pnl}")

    # ==========================
    # CERRAR MANUAL
    # ==========================

    def close_position(self, symbol, price):

        if symbol not in self.positions:
            return

        self._close_and_record(symbol, price)

    # ==========================
    # SL / TP AUTOMÁTICO
    # ==========================

    def check_positions(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        side = pos.get("side", "BUY")

        if side == "BUY":

            if price <= pos["sl"]:
                print(f"STOP LOSS {symbol}")
                self._close_and_record(symbol, price)
                return

            if price >= pos["tp"]:
                print(f"TAKE PROFIT {symbol}")
                self._close_and_record(symbol, price)
                return

        else:

            if price >= pos["sl"]:
                print(f"STOP LOSS {symbol}")
                self._close_and_record(symbol, price)
                return

            if price <= pos["tp"]:
                print(f"TAKE PROFIT {symbol}")
                self._close_and_record(symbol, price)
                return