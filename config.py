
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///trades.db")
START_BALANCE = float(os.getenv("START_BALANCE", 10000))
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", 0.01))
MAX_OPEN_TRADES = int(os.getenv("MAX_OPEN_TRADES", 5))
LOOP_INTERVAL = int(os.getenv("LOOP_INTERVAL", 3600))
