def open_trade(state, symbol, side, entry, sl, tp, size):
    trade = {
        "symbol": symbol,
        "side": side,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "size": size
    }

    state.open_trades.append(trade)
    print(f"OPEN {side} {symbol} @ {entry}", flush=True)
    state.save()

def check_closures(state, price_map):
    closed = []

    for trade in state.open_trades:
        price = price_map.get(trade["symbol"])
        if not price:
            continue

        if trade["side"] == "BUY":
            if price <= trade["sl"] or price >= trade["tp"]:
                pnl = (price - trade["entry"]) * trade["size"]
                state.balance += pnl
                closed.append(trade)

        if trade["side"] == "SELL":
            if price >= trade["sl"] or price <= trade["tp"]:
                pnl = (trade["entry"] - price) * trade["size"]
                state.balance += pnl
                closed.append(trade)

    for t in closed:
        state.open_trades.remove(t)
        state.trades.append(t)
        print(f"CLOSE {t['symbol']}", flush=True)

    if closed:
        state.save()