
from sklearn.ensemble import RandomForestClassifier
import numpy as np

model = RandomForestClassifier()
trained=False

def train(df):
    global trained
    df['returns']=df['close'].pct_change()
    df=df.dropna()
    if len(df)<50:
        return
    X=df[['returns']]
    y=(df['returns'].shift(-1)>0).astype(int)
    model.fit(X[:-1],y[:-1])
    trained=True

def filter_signal(df):
    if not trained:
        return True
    val=np.array([[df['close'].pct_change().iloc[-1]]])
    pred=model.predict(val)
    return pred[0]==1
