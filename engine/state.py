
from config import START_BALANCE

class BotState:
    def __init__(self):
        self.balance = START_BALANCE
        self.equity = START_BALANCE
        self.open_positions = []
        self.trade_history = []
        self.max_equity = START_BALANCE
        self.drawdown = 0
        self.winrate = 0
        self.profit_factor = 0
        self.ai_status = "running"
