import pandas as pd

from src.risk_engine import RiskEngine, RiskConfig
from src.state_manager import StateManager

DATA_PATH = "datas/btc_4h_full.csv"
MODEL_PATH = "models/tail_model_v1.pkl"


engine = RiskEngine(RiskConfig(), MODEL_PATH)
state_manager = StateManager()


# ===== Load state =====

state = state_manager.load_state()

if state is None:
    print("Initializing state from historical data")

    df = pd.read_csv(DATA_PATH)

    state = engine.initialize_state(df)

    state_manager.save_state(state)

else:
    print("Loaded existing state")


# ===== Simulate new candle =====

df = pd.read_csv(DATA_PATH)
new_candle = df.iloc[-1].to_dict()

result, state = engine.update_with_new_candle(state, new_candle)

state_manager.save_state(state)

print("Tail Prob:", result["tail_prob"])
print("Regime:", result["regime"])
print("Exposure:", result["exposure"])