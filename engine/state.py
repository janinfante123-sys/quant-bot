import json
import os
from config import START_BALANCE

STATE_FILE = "state.json"

class BotState:
    def __init__(self):
        if os.path.exists(STATE_FILE):
            self.load()
        else:
            self.balance = START_BALANCE
            self.open_trades = []
            self.trades = []
            self.save()

    def save(self):
        data = {
            "balance": self.balance,
            "open_trades": self.open_trades,
            "trades": self.trades
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f)

    def load(self):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)

        self.balance = data.get("balance", START_BALANCE)
        self.open_trades = data.get("open_trades", [])
        self.trades = data.get("trades", [])