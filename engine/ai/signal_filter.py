
import random

class SignalFilter:

    def score(self,signal,data):

        base=random.random()

        vol=data.close.pct_change().std()

        if signal=="BUY":
            base+=0.2

        if vol>0.02:
            base-=0.2

        return base
