import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime

from src.indicators import compute_indicators

MODEL_VERSION = "v1.0"

df = pd.read_csv("datas/btc_4h_full.csv")

df = compute_indicators(df, 14, 200)

df["fwd_ret"] = df["close"].pct_change().shift(-1)
df["tail_event"] = (df["fwd_ret"] <= -0.05).astype(int)

df = df.dropna()

features = ["atr"]

X = df[features]
y = df["tail_event"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipeline.fit(X, y)

artifact = {
    "pipeline": pipeline,
    "features": features,
    "model_version": MODEL_VERSION,
    "trained_at": datetime.utcnow().isoformat()
}

joblib.dump(artifact, "models/tail_model_v1.pkl")

print("Model trained and saved successfully.")