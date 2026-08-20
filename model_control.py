import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

EPS = 1e-8

def _safe_ratio(a, b):
    return a / (np.abs(b) + EPS)

def build_control_features(df, feature_columns, horizons=(1, 3, 7, 23)):
    x = df[feature_columns].astype(float).copy()
    out = pd.DataFrame(index=df.index)

    for c in feature_columns:
        out[f"{c}__x"] = x[c]
        out[f"{c}__dx"] = x[c].diff()
        out[f"{c}__ddx"] = x[c].diff().diff()

    for i, a in enumerate(feature_columns):
        for b in feature_columns[i+1:]:
            out[f"rel__{a}__{b}__diff"] = x[a] - x[b]
            out[f"rel__{a}__{b}__ratio"] = _safe_ratio(x[a], x[b])
            out[f"rel__{a}__{b}__product"] = x[a] * x[b]

    base_cols = list(out.columns)
    for h in horizons:
        for c in base_cols:
            out[f"{c}__mean{h}"] = out[c].rolling(h, min_periods=1).mean()
            out[f"{c}__std{h}"] = out[c].rolling(h, min_periods=1).std().fillna(0.0)

    return out.replace([np.inf, -np.inf], np.nan).fillna(0.0)

class ControlModel:
    def __init__(self, random_state=23):
        self.scaler = RobustScaler()
        self.model = LogisticRegression(max_iter=4000, random_state=random_state)
        self.columns_ = None

    def fit(self, X, y):
        self.columns_ = list(X.columns)
        Xs = self.scaler.fit_transform(X)
        self.model.fit(Xs, y)
        return self

    def predict_proba(self, X):
        X = X.reindex(columns=self.columns_, fill_value=0)
        Xs = self.scaler.transform(X)
        return self.model.predict_proba(Xs)[:, 1]
