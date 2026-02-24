class Portfolio:

    def __init__(self, capital):
        self.initial = capital
        self.cash = capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.max_equity = capital
        self.drawdown = 0

    def open_position(self, symbol, entry, stop, risk_pct):
        risk_amount = self.cash * risk_pct
        risk_per_unit = abs(entry - stop)

        if risk_per_unit == 0:
            return

        size = risk_amount / risk_per_unit

        self.positions[symbol] = {
            "entry": entry,
            "stop": stop,
            "size": size
        }

    def close_position(self, symbol, price):
        pos = self.positions[symbol]
        pnl = (price - pos["entry"]) * pos["size"]

        self.cash += pnl

        self.trades.append({
            "symbol": symbol,
            "entry": pos["entry"],
            "exit": price,
            "pnl": pnl
        })

        del self.positions[symbol]

    def update_equity(self):
        equity = self.cash
        self.equity_curve.append(equity)

        if equity > self.max_equity:
            self.max_equity = equity

        self.drawdown = (self.max_equity - equity) / self.max_equity
