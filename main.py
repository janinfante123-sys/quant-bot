
from engine.data.data_feed import DataFeed
from engine.strategies.trend import TrendStrategy
from engine.strategies.mean_reversion import MeanReversion
from engine.ai.signal_filter import SignalFilter
from engine.risk.risk_manager import RiskManager
from engine.portfolio.portfolio import Portfolio
from engine.execution.executor import Executor
from engine.metrics import Metrics
from config.settings import ASSETS, CAPITAL

def run():

    datafeed=DataFeed()
    trend=TrendStrategy()
    meanrev=MeanReversion()
    ai=SignalFilter()
    risk=RiskManager()

    portfolio=Portfolio(CAPITAL)
    executor=Executor(portfolio)

    for symbol in ASSETS:

        df=datafeed.synthetic()

        signal=trend.signal(df)

        score=ai.score(signal,df)

        if score<0.5:
            continue

        size=risk.position_size(portfolio.capital,df)

        price=df.close.iloc[-1]

        executor.execute(symbol,signal,size,price)

    metrics=Metrics()

    print(metrics.report(portfolio.trades))

if __name__=="__main__":
    run()
