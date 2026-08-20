import pandas as pd
from tortoise import TortoiseExperiment
from model_full import build_full_features
from model_control import build_control_features

def test_feature_builders():
    df = pd.read_csv("example_data.csv")
    cols = ["sensor_a", "sensor_b", "sensor_c"]
    full = build_full_features(df, cols)
    ctrl = build_control_features(df, cols)
    assert len(full) == len(df)
    assert len(ctrl) == len(df)
    assert "coherence" in full.columns
    assert "coherence" not in ctrl.columns

def test_experiment_runs():
    df = pd.read_csv("example_data.csv")
    exp = TortoiseExperiment(
        target_column="failure",
        time_column="time",
        feature_columns=["sensor_a", "sensor_b", "sensor_c"],
    )
    result = exp.run(df)
    assert "full" in result
    assert "control" in result
    assert "delta_brier_control_minus_full" in result
