from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Position:
    symbol: str
    side: str
    entry: float
    size: float
    sl: float
    tp: float

@dataclass
class BotState:
    balance: float = 1_000_000
    equity: float = 1_000_000
    risk_per_trade: float = 0.01

    positions: Dict[str, Position] = field(default_factory=dict)
    trade_history: List[dict] = field(default_factory=list)
    last_candle_time: Dict[str, str] = field(default_factory=dict)

state = BotState()
