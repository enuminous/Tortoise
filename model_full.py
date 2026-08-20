import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

EPS = 1e-8

def _safe_ratio(a, b):
    return a / (np.abs(b) + EPS)

def build_full_features(df, feature_columns, horizons=(1, 3, 7, 23)):
    x = df[feature_columns].astype(float).copy()
    out = pd.DataFrame(index=df.index)

    # Local state, velocity, acceleration.
    for c in feature_columns:
        out[f"{c}__x"] = x[c]
        out[f"{c}__dx"] = x[c].diff()
        out[f"{c}__ddx"] = x[c].diff().diff()

    # Pairwise relational state.
    rel_cols = []
    for i, a in enumerate(feature_columns):
        for b in feature_columns[i+1:]:
            d = f"rel__{a}__{b}__diff"
            r = f"rel__{a}__{b}__ratio"
            p = f"rel__{a}__{b}__product"
            out[d] = x[a] - x[b]
            out[r] = _safe_ratio(x[a], x[b])
            out[p] = x[a] * x[b]
            rel_cols.extend([d, r, p])

    # Multiscale memories.
    base_cols = list(out.columns)
    for h in horizons:
        for c in base_cols:
            out[f"{c}__mean{h}"] = out[c].rolling(h, min_periods=1).mean()
            out[f"{c}__std{h}"] = out[c].rolling(h, min_periods=1).std().fillna(0.0)

    # Contradiction / coherence from rolling expected relational state.
    contradiction_cols = []
    for c in rel_cols:
        expected = out[c].rolling(max(horizons), min_periods=3).median()
        dev = out[c] - expected
        mad = dev.abs().rolling(max(horizons), min_periods=3).median()
        contradiction = dev.abs() / (1.4826 * mad + EPS)
        cc = f"{c}__contradiction"
        out[cc] = contradiction
        contradiction_cols.append(cc)

    if contradiction_cols:
        coherence_parts = [np.exp(-out[c].clip(lower=0)) for c in contradiction_cols]
        coherence = pd.concat(coherence_parts, axis=1).mean(axis=1)
    else:
        coherence = pd.Series(1.0, index=out.index)

    out["coherence"] = coherence
    out["coherence_velocity"] = coherence.diff()
    out["coherence_acceleration"] = coherence.diff().diff()

    # Compact recursive state.
    state = pd.concat(
        [
            out["coherence"],
            out["coherence_velocity"].fillna(0),
            out["coherence_acceleration"].fillna(0),
        ],
        axis=1,
    ).fillna(0).to_numpy()

    recurrent = np.zeros_like(state)
    for t in range(len(state)):
        prev = recurrent[t-1] if t > 0 else np.zeros(state.shape[1])
        s = state[t].copy()
        for _ in range(3):
            s = 0.5 * s + 0.5 * np.tanh(s + prev)
        recurrent[t] = s

    out["recursive_coherence"] = recurrent[:, 0]
    out["recursive_velocity"] = recurrent[:, 1]
    out["recursive_acceleration"] = recurrent[:, 2]

    return out.replace([np.inf, -np.inf], np.nan).fillna(0.0)

class FullTortoiseModel:
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
