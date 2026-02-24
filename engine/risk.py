class RiskManager:

    def __init__(self):
        self.max_dd = 0.15

    def allow_trade(self, portfolio):
        if portfolio.drawdown > self.max_dd:
            return False
        return True
