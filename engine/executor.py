
from engine.database import Session, Trade

def execute(state,symbol,direction,entry,sl,tp,size):
    trade={
        "symbol":symbol,
        "direction":direction,
        "entry":entry,
        "sl":sl,
        "tp":tp,
        "size":size
    }
    state.open_positions.append(trade)

def check_closures(state, price_map):
    for trade in state.open_positions[:]:
        price = price_map.get(trade["symbol"])
        if price is None:
            continue

        if trade["direction"]=="BUY":
            if price<=trade["sl"] or price>=trade["tp"]:
                close(state,trade,price)
        else:
            if price>=trade["sl"] or price<=trade["tp"]:
                close(state,trade,price)

def close(state,trade,exit_price):
    profit=(exit_price-trade["entry"])*trade["size"]
    if trade["direction"]=="SELL":
        profit*=-1

    state.balance+=profit
    state.trade_history.append(profit)

    db=Session()
    db.add(Trade(symbol=trade["symbol"],direction=trade["direction"],entry=trade["entry"],exit=exit_price,profit=profit))
    db.commit()
    db.close()

    state.open_positions.remove(trade)
