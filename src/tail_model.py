import joblib
import pandas as pd
import numpy as np


class TailModel:

    def __init__(self, model_path: str):
        artifact = joblib.load(model_path)

        self.pipeline = artifact["pipeline"]
        self.features = artifact["features"]
        self.model_version = artifact.get("model_version", "unknown")

    def predict_proba(self, df: pd.DataFrame) -> float:

        X = df[self.features]

        if X.isna().any().any():
            return np.nan

        return self.pipeline.predict_proba(X)[0, 1]