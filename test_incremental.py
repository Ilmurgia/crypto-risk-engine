import pandas as pd
from src.risk_engine import RiskEngine, RiskConfig

df = pd.read_csv("datas/btc_4h_full.csv")

engine = RiskEngine(
    RiskConfig(),
    model_path="models/tail_model_v1.pkl"
)

# === Initialize with historical data ===
historical = df.iloc[:-1]
state = engine.initialize_state(historical)

# === Simulate new candle ===
new_candle = df.iloc[-1].to_dict()

result, new_state = engine.update_with_new_candle(state, new_candle)

print("Tail Prob:", result["tail_prob"])
print("Regime:", result["regime"])
print("Exposure:", result["exposure"])