import pandas as pd
from fastapi import FastAPI

from src.risk_engine import RiskEngine, RiskConfig
from src.state_manager import StateManager
from apscheduler.schedulers.background import BackgroundScheduler
from src.data_fetcher import get_latest_candle

MODEL_PATH = "models/tail_model_v1.pkl"
DATA_PATH = "datas/btc_4h_full.csv"

engine = RiskEngine(RiskConfig(), MODEL_PATH)
state_manager = StateManager()

app = FastAPI()


# ---- load or initialize state ----

state = state_manager.load_state()

if state is None:
    df = pd.read_csv(DATA_PATH)
    state = engine.initialize_state(df)
    state_manager.save_state(state)


# ---- endpoints ----

@app.get("/")
def health():
    return {"status": "running"}


@app.get("/signal")
def get_signal():
    return state


@app.post("/update")
def update_signal(candle: dict):

    global state

    result, state = engine.update_with_new_candle(state, candle)

    state_manager.save_state(state)

    return result

def scheduled_update():

    global state

    candle = get_latest_candle()

    result, state = engine.update_with_new_candle(state, candle)

    state_manager.save_state(state)

    print("AUTO UPDATE:", result)

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        scheduled_update,
        "interval",
        hours=4
    )

    scheduler.start()