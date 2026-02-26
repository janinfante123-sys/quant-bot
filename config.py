# ==============================
# CONFIG
# ==============================

# Mercados activos
SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "AAPL"
]

# Intervalo del loop (segundos)
# 900 = 15 minutos
LOOP_INTERVAL = 900

# Capital inicial paper trading
START_BALANCE = 1000

# Timeframe datos
DATA_INTERVAL = "1h"
DATA_LOOKBACK = "7d"

# Tamaño por trade (porcentaje del balance)
RISK_PER_TRADE = 0.1   # 10%