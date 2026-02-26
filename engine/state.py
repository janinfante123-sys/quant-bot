class BotState:

    def __init__(self):
        self.balance = 1000
        self.positions = {}

    def open_position(self, symbol, price):

        if symbol in self.positions:
            return

        size = self.balance * 0.1  # 10% del balance

        if size <= 0:
            return

        self.positions[symbol] = {
            "entry": float(price),
            "size": size
        }

        self.balance -= size

        print(f"OPEN {symbol} @ {price}")

    def close_position(self, symbol, price):

        if symbol not in self.positions:
            return

        entry = self.positions[symbol]["entry"]
        size = self.positions[symbol]["size"]

        # beneficio real
        pnl = size * ((price - entry) / entry)

        # devolvemos tamaño + beneficio
        self.balance += size + pnl

        del self.positions[symbol]

        print(f"CLOSE {symbol} @ {price}")
