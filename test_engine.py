import pandas as pd
from src.risk_engine import RiskEngine, RiskConfig

df = pd.read_csv("datas/btc_4h_full.csv")

engine = RiskEngine(
    RiskConfig(),
    model_path="models/tail_model_v1.pkl"
)

result = engine.run(df)

print(result[["close", "tail_prob", "regime", "exposure"]].tail())
print("Non-NaN exposure:", result["exposure"].notna().sum())