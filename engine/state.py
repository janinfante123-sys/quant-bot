class BotState:

    def __init__(self):
        self.balance = 1000
        self.positions = {}

    # ======================================
    # CALCULAR TAMAÑO CON RIESGO 1%
    # ======================================
    def _calc_size(self, entry, sl):
        risk_amount = self.balance * 0.01
        risk_per_unit = abs(entry - sl)

        if risk_per_unit == 0:
            return 0

        size = risk_amount / risk_per_unit
        return size

    # ======================================
    # ABRIR POSICIÓN
    # ======================================
    def open_position(self, symbol, price):

        if symbol in self.positions:
            return

        # SL 1%
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

        print(f"OPEN {symbol} @ {price} SL:{sl} TP:{tp}")

    # ======================================
    # CERRAR MANUAL (por señal contraria)
    # ======================================
    def close_position(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        entry = pos["entry"]
        size = pos["size"]

        pnl = size * ((price - entry) / entry)
        self.balance += pnl

        del self.positions[symbol]

        print(f"CLOSE {symbol} @ {price} PnL:{pnl}")

    # ======================================
    # CHECK SL/TP AUTOMÁTICO
    # ======================================
    def check_positions(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        if price <= pos["sl"]:
            pnl = pos["size"] * ((price - pos["entry"]) / pos["entry"])
            self.balance += pnl
            print(f"STOP LOSS {symbol} PnL:{pnl}")
            del self.positions[symbol]
            return

        if price >= pos["tp"]:
            pnl = pos["size"] * ((price - pos["entry"]) / pos["entry"])
            self.balance += pnl
            print(f"TAKE PROFIT {symbol} PnL:{pnl}")
            del self.positions[symbol]
            return
