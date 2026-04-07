class Metrics:

    def __init__(self):
        self.trades = []
        self.total_pnl = 0
        self.wins = 0
        self.losses = 0

    def record_trade(self, symbol, entry, exit_price, size, pnl):

        trade = {
            "symbol": symbol,
            "entry": entry,
            "exit": exit_price,
            "size": size,
            "pnl": pnl
        }

        self.trades.append(trade)
        self.total_pnl += pnl

        if pnl > 0:
            self.wins += 1
        else:
            self.losses += 1

        print(f"📊 Trade recorded | PnL: {round(pnl, 2)}")

    def summary(self):

        total = len(self.trades)
        winrate = (self.wins / total * 100) if total > 0 else 0

        return {
            "trades": total,
            "wins": self.wins,
            "losses": self.losses,
            "winrate": round(winrate, 2),
            "total_pnl": round(self.total_pnl, 2)
        }