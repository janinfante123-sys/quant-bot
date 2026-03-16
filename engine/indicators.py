
class Indicators:

    def sma(self,data,p):
        return data.close.rolling(p).mean()

    def ema(self,data,p):
        return data.close.ewm(span=p).mean()

    def rsi(self,data,p=14):

        delta=data.close.diff()

        gain=delta.clip(lower=0)
        loss=-delta.clip(upper=0)

        rs=gain.rolling(p).mean()/loss.rolling(p).mean()

        return 100-(100/(1+rs))

    def atr(self,data,p=14):

        tr=data.high-data.low

        return tr.rolling(p).mean()
