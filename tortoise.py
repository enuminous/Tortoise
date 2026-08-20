from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from model_full import build_full_features, FullTortoiseModel
from model_control import build_control_features, ControlModel
from baselines import BaseRateModel, LogisticBaseline
from metrics import binary_metrics

@dataclass
class TortoiseExperiment:
    target_column: str
    feature_columns: list
    time_column: str | None = None
    horizons: tuple = (1, 3, 7, 23)
    test_size: float = 0.30
    random_state: int = 23

    def _ordered_split(self, df):
        if self.time_column is not None:
            df = df.sort_values(self.time_column).reset_index(drop=True)
            cut = max(1, int(len(df) * (1 - self.test_size)))
            return df.iloc[:cut].copy(), df.iloc[cut:].copy()
        train, test = train_test_split(
            df,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=False,
        )
        return train.copy(), test.copy()

    def run(self, df):
        train_df, test_df = self._ordered_split(df)
        y_train = train_df[self.target_column].astype(int).to_numpy()
        y_test = test_df[self.target_column].astype(int).to_numpy()

        combined = pd.concat([train_df, test_df], axis=0, ignore_index=True)
        full_all = build_full_features(combined, self.feature_columns, self.horizons)
        ctrl_all = build_control_features(combined, self.feature_columns, self.horizons)

        ntrain = len(train_df)
        Xf_train, Xf_test = full_all.iloc[:ntrain], full_all.iloc[ntrain:]
        Xc_train, Xc_test = ctrl_all.iloc[:ntrain], ctrl_all.iloc[ntrain:]

        full = FullTortoiseModel(self.random_state).fit(Xf_train, y_train)
        ctrl = ControlModel(self.random_state).fit(Xc_train, y_train)

        base = BaseRateModel().fit(train_df[self.feature_columns], y_train)
        logistic = LogisticBaseline(self.random_state).fit(
            train_df[self.feature_columns].astype(float), y_train
        )

        p_full = full.predict_proba(Xf_test)
        p_ctrl = ctrl.predict_proba(Xc_test)
        p_base = base.predict_proba(test_df[self.feature_columns])
        p_log = logistic.predict_proba(test_df[self.feature_columns].astype(float))

        mf = binary_metrics(y_test, p_full)
        mc = binary_metrics(y_test, p_ctrl)
        mb = binary_metrics(y_test, p_base)
        ml = binary_metrics(y_test, p_log)

        return {
            "n_train": len(train_df),
            "n_test": len(test_df),
            "full": mf,
            "control": mc,
            "base_rate": mb,
            "logistic": ml,
            "delta_brier_control_minus_full": mc["brier"] - mf["brier"],
            "interpretation": (
                "positive favors TORTOISE-M1; zero indicates no incremental Brier advantage; "
                "negative favors the matched non-EFMW control"
            ),
        }
