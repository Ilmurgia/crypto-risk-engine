import pandas as pd
from src.indicators import compute_indicators
from src.regime import compute_regime
from src.tail_model import compute_tail_probability

df = pd.read_csv("datas/btc_4h_full.csv")

df = compute_indicators(df, atr_window=14, ema_window=200)
df = compute_regime(df)

df = compute_tail_probability(
    df,
    threshold=0.05,
    window=500
)

print(df[["close", "tail_prob"]].iloc[18000:18010])
print("Non-NaN tail_prob:", df["tail_prob"].notna().sum())