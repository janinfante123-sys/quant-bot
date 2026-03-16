
from ..indicators import Indicators

class TrendStrategy:

    def __init__(self):
        self.ind = Indicators()

    def signal(self,data):

        fast=self.ind.sma(data,20)
        slow=self.ind.sma(data,50)

        if fast.iloc[-1] > slow.iloc[-1]:
            return "BUY"

        if fast.iloc[-1] < slow.iloc[-1]:
            return "SELL"

        return "HOLD"
