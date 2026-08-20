import numpy as np
from sklearn.metrics import (
    brier_score_loss,
    log_loss,
    roc_auc_score,
    average_precision_score,
    accuracy_score,
)

def calibration_error(y_true, p, bins=10):
    y_true = np.asarray(y_true, dtype=float)
    p = np.asarray(p, dtype=float)
    edges = np.linspace(0.0, 1.0, bins + 1)
    ids = np.digitize(p, edges[1:-1], right=True)
    total = len(p)
    err = 0.0
    for b in range(bins):
        mask = ids == b
        if not np.any(mask):
            continue
        err += (mask.sum() / total) * abs(p[mask].mean() - y_true[mask].mean())
    return float(err)

def binary_metrics(y_true, p):
    y_true = np.asarray(y_true, dtype=int)
    p = np.clip(np.asarray(p, dtype=float), 1e-9, 1 - 1e-9)
    out = {
        "brier": float(brier_score_loss(y_true, p)),
        "log_loss": float(log_loss(y_true, np.c_[1-p, p], labels=[0, 1])),
        "accuracy_0.5": float(accuracy_score(y_true, (p >= 0.5).astype(int))),
        "calibration_error": calibration_error(y_true, p),
    }
    if len(np.unique(y_true)) > 1:
        out["roc_auc"] = float(roc_auc_score(y_true, p))
        out["average_precision"] = float(average_precision_score(y_true, p))
    else:
        out["roc_auc"] = None
        out["average_precision"] = None
    return out
