import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

class BaseRateModel:
    def fit(self, X, y):
        self.p_ = float(np.mean(y))
        return self

    def predict_proba(self, X):
        return np.full(len(X), self.p_, dtype=float)

class LogisticBaseline:
    def __init__(self, random_state=23):
        self.scaler = RobustScaler()
        self.model = LogisticRegression(max_iter=4000, random_state=random_state)

    def fit(self, X, y):
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X), y)
        return self

    def predict_proba(self, X):
        return self.model.predict_proba(self.scaler.transform(X))[:, 1]
