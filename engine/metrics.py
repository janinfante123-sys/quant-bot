
import numpy as np

class Metrics:

    def report(self,trades):

        if len(trades)==0:
            return {}

        wins=[t for t in trades if t>0]
        losses=[t for t in trades if t<0]

        winrate=len(wins)/len(trades)

        pf=sum(wins)/abs(sum(losses)) if losses else 0

        sharpe=np.mean(trades)/np.std(trades) if np.std(trades)!=0 else 0

        return {
            "trades":len(trades),
            "winrate":winrate,
            "profit_factor":pf,
            "sharpe":sharpe
        }
