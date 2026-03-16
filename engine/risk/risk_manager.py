
class RiskManager:

    def position_size(self,capital,data):

        atr=(data.high-data.low).rolling(14).mean().iloc[-1]

        if atr == 0:
            return 0

        risk=capital*0.01

        return risk/(atr*2)
