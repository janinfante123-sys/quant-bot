
from ..indicators import Indicators

class MeanReversion:

    def __init__(self):
        self.ind = Indicators()

    def signal(self,data):

        rsi=self.ind.rsi(data)

        if rsi.iloc[-1] < 30:
            return "BUY"

        if rsi.iloc[-1] > 70:
            return "SELL"

        return "HOLD"
