from config import START_BALANCE

class BotState:
    def __init__(self):
        self.balance = START_BALANCE
        self.open_trades = []
        self.trades = []