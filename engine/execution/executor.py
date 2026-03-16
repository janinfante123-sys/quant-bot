
class Executor:

    def __init__(self,portfolio):
        self.portfolio=portfolio

    def execute(self,symbol,signal,size,price):

        if signal=="BUY" and symbol not in self.portfolio.positions:
            self.portfolio.open(symbol,size,price)

        if signal=="SELL" and symbol in self.portfolio.positions:
            self.portfolio.close(symbol,price)
