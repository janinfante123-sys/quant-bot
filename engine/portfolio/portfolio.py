
class Portfolio:

    def __init__(self,capital):

        self.capital=capital
        self.positions={}
        self.trades=[]

    def open(self,symbol,size,price):

        self.positions[symbol]=(size,price)

    def close(self,symbol,price):

        size,entry=self.positions[symbol]

        pnl=(price-entry)*size

        self.capital+=pnl

        self.trades.append(pnl)

        del self.positions[symbol]
