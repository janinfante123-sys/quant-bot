
def update(state):
    state.equity=state.balance
    if state.equity>state.max_equity:
        state.max_equity=state.equity
    state.drawdown=(state.max_equity-state.equity)/state.max_equity if state.max_equity>0 else 0
