
from config import RISK_PER_TRADE

def position_size(balance, entry, stop):
    risk_amount = balance * RISK_PER_TRADE
    risk_per_unit = abs(entry - stop)
    if risk_per_unit == 0:
        return 0
    return round(risk_amount / risk_per_unit, 4)

def dynamic_sl_tp(entry, direction):
    if direction == "BUY":
        return entry*0.98, entry*1.04
    else:
        return entry*1.02, entry*0.96
