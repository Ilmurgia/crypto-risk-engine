import pandas as pd
import numpy as np

# === LOAD FULL DATASET ===
df = pd.read_csv("datas/btc_4h_full.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# === ATR CALCULATION ===
df["previous_close"] = df["close"].shift(1)
df["tr1"] = df["high"] - df["low"]
df["tr2"] = (df["high"] - df["previous_close"]).abs()
df["tr3"] = (df["low"] - df["previous_close"]).abs()
df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
df["atr_14"] = df["true_range"].rolling(window=14).mean()

# === TARGET ===
df["future_close"] = df["close"].shift(-6)
df["future_return"] = (df["future_close"] - df["close"]) / df["close"]
df["target"] = (df["future_return"].abs() > 0.025).astype(int)

# === LOG RETURN ===
df["log_return"] = np.log(df["close"] / df["close"].shift(1))

# === CLEAN ===
df = df.dropna()

# === SAVE ===
df.to_csv("datas/btc_4h_full_features.csv", index=False)

print("Righe finali:", len(df))
print("Percentuale target=1:", df["target"].mean())
print("Colonne:", df.columns)