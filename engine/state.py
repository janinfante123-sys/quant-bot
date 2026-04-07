import json
import os
from engine.metrics import Metrics


class BotState:

    FILE = "bot_state.json"
    MAX_POSITIONS = 4
    COOLDOWN_CYCLES = 2

    def __init__(self):
        self.balance = 1000
        self.positions = {}
        self.cooldowns = {}
        self.metrics = Metrics()
        self._load()

    # ==========================
    # PERSISTENCIA
    # ==========================

    def _save(self):
        data = {
            "balance": self.balance,
            "positions": self.positions,
            "cooldowns": self.cooldowns
        }
        with open(self.FILE, "w") as f:
            json.dump(data, f)

    def _load(self):
        if os.path.exists(self.FILE):
            with open(self.FILE, "r") as f:
                data = json.load(f)
                self.balance = data.get("balance", 1000)
                self.positions = data.get("positions", {})
                self.cooldowns = data.get("cooldowns", {})
                print("🔄 STATE RESTORED")

    # ==========================
    # COOLDOWN
    # ==========================

    def update_cooldowns(self):
        for symbol in list(self.cooldowns.keys()):
            self.cooldowns[symbol] -= 1
            if self.cooldowns[symbol] <= 0:
                del self.cooldowns[symbol]

    def in_cooldown(self, symbol):
        return symbol in self.cooldowns

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
    # ABRIR POSICIÓN (ATR)
    # ==========================

    def open_position(self, symbol, price, side="BUY", atr=0):

        if symbol in self.positions:
            return

        if self.in_cooldown(symbol):
            print(f"⏳ {symbol} in cooldown")
            return

        if len(self.positions) >= self.MAX_POSITIONS:
            print("⚠️ MAX POSITIONS REACHED")
            return

        # 🔥 fallback si no hay ATR
        if atr is None or atr == 0:
            atr = price * 0.005  # 0.5% fallback

        # 🔥 SL/TP dinámico con ATR
        if side == "BUY":
            sl = price - (atr * 2)
            tp = price + (atr * 4)
        else:
            sl = price + (atr * 2)
            tp = price - (atr * 4)

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
    # CIERRE
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

        self.cooldowns[symbol] = self.COOLDOWN_CYCLES

        del self.positions[symbol]
        self._save()

        print(f"CLOSE {symbol} @ {price} PnL:{pnl}")

    # ==========================
    # CIERRE MANUAL
    # ==========================

    def close_position(self, symbol, price):

        if symbol not in self.positions:
            return

        self._close_and_record(symbol, price)

    # ==========================
    # SL / TP
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