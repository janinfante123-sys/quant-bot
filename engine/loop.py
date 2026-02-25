
import time
from engine import data_feed,strategy,risk,executor,ai_module,metrics
from config import MAX_OPEN_TRADES, LOOP_INTERVAL

SYMBOLS=[
("crypto","BTC/USDT"),
("crypto","ETH/USDT"),
("stock","AAPL"),
("stock","MSFT"),
("forex","EURUSD")
]

def get_price(market,symbol):
    if market=="crypto":
        df=data_feed.get_crypto(symbol)
    elif market=="stock":
        df=data_feed.get_stock(symbol)
    else:
        df=data_feed.get_forex(symbol)
    return df, df['close'].iloc[-1]

def run(state):
    print("🟢 BOT LOOP STARTED")

    while True:
        try:
            print("🔁 NEW CYCLE")

            price_map={}
            for market,symbol in SYMBOLS:
                print(f"Checking {symbol}")

                df,price=get_price(market,symbol)
                price_map[symbol]=price

                if not ai_module.trained:
                    ai_module.train(df)

                signal=strategy.generate_signal(df)
                if signal!="HOLD" and ai_module.filter_signal(df):
                    entry=price
                    sl,tp=risk.dynamic_sl_tp(entry,signal)
                    size=risk.position_size(state.balance,entry,sl)
                    if size>0:
                        executor.execute(state,symbol,signal,entry,sl,tp,size)

            executor.check_closures(state,price_map)
            metrics.update(state)

            print("⏳ sleeping...")
            time.sleep(LOOP_INTERVAL)

        except Exception as e:
            print("❌ LOOP ERROR:", e)
            time.sleep(5)
