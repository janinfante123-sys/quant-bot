
import numpy as np

def simulate(trades,n=1000):

    if len(trades)==0:
        return 0

    results=[]

    for _ in range(n):

        sample=np.random.choice(trades,len(trades))

        results.append(sum(sample))

    return np.mean(results)
