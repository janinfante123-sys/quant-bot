import numpy as np

def metrics(portfolio):

    trades = portfolio.trades

    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]

    win_rate = len(wins)/len(trades) if trades else 0

    total_profit = sum(t["pnl"] for t in wins)
    total_loss = abs(sum(t["pnl"] for t in losses))

    pf = total_profit/total_loss if total_loss else 0

    returns = np.diff(portfolio.equity_curve)
    sharpe = (np.mean(returns)/np.std(returns)) if len(returns)>2 else 0

    return {
        "win_rate": round(win_rate,2),
        "profit_factor": round(pf,2),
        "sharpe": round(sharpe,2),
        "drawdown": round(portfolio.drawdown,3)
    }
