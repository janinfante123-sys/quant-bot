def position_size(balance, risk_per_trade, entry, stop):
    risk_amount = balance * risk_per_trade
    risk_per_unit = abs(entry - stop)

    if risk_per_unit == 0:
        return 0

    size = risk_amount / risk_per_unit
    return size