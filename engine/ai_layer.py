import numpy as np

class AdaptiveAI:

    def __init__(self):
        self.base_risk = 0.01
        self.current_risk = 0.01
        self.regime = "normal"

    def detect_regime(self, df):
        returns = df["close"].pct_change().dropna()
        vol = np.std(returns[-50:])
        trend = abs(df["close"].iloc[-1] - df["close"].iloc[-50])

        if vol > 0.03:
            self.regime = "high_vol"
        elif trend < 0.01 * df["close"].iloc[-1]:
            self.regime = "range"
        else:
            self.regime = "trend"

    def adjust_risk(self, portfolio):
        dd = portfolio.drawdown

        if dd > 0.1:
            self.current_risk = 0.005
        elif self.regime == "trend":
            self.current_risk = 0.012
        elif self.regime == "range":
            self.current_risk = 0.008
        else:
            self.current_risk = self.base_risk

        return self.current_risk
