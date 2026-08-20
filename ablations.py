import numpy as np
import pandas as pd
from model_full import build_full_features
from model_control import build_control_features

def no_recursion(df, feature_columns, horizons=(1,3,7,23)):
    x = build_full_features(df, feature_columns, horizons)
    return x.drop(
        columns=[c for c in x.columns if c.startswith("recursive_")],
        errors="ignore",
    )

def no_coherence(df, feature_columns, horizons=(1,3,7,23)):
    x = build_full_features(df, feature_columns, horizons)
    drop = [c for c in x.columns if "coherence" in c or c.startswith("recursive_")]
    return x.drop(columns=drop, errors="ignore")

def no_contradiction(df, feature_columns, horizons=(1,3,7,23)):
    x = build_full_features(df, feature_columns, horizons)
    drop = [c for c in x.columns if "contradiction" in c or "coherence" in c or c.startswith("recursive_")]
    return x.drop(columns=drop, errors="ignore")

def no_relations(df, feature_columns, horizons=(1,3,7,23)):
    x = build_control_features(df, feature_columns, horizons)
    drop = [c for c in x.columns if c.startswith("rel__")]
    return x.drop(columns=drop, errors="ignore")

def short_memory(df, feature_columns):
    return build_full_features(df, feature_columns, horizons=(1,))

def shuffled_time(df, feature_columns, horizons=(1,3,7,23), random_state=23):
    rng = np.random.default_rng(random_state)
    shuffled = df.copy()
    perm = rng.permutation(len(shuffled))
    shuffled.loc[:, feature_columns] = shuffled[feature_columns].to_numpy()[perm]
    return build_full_features(shuffled, feature_columns, horizons)

def shuffled_relations(df, feature_columns, horizons=(1,3,7,23), random_state=23):
    rng = np.random.default_rng(random_state)
    altered = df.copy()
    for c in feature_columns:
        altered[c] = rng.permutation(altered[c].to_numpy())
    return build_full_features(altered, feature_columns, horizons)
