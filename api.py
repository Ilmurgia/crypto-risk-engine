import pandas as pd
from fastapi import FastAPI

from src.risk_engine import RiskEngine, RiskConfig
from src.state_manager import StateManager
from apscheduler.schedulers.background import BackgroundScheduler
from src.data_fetcher import get_latest_candle

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
MODEL_PATH = "models/tail_model_v1.pkl"
DATA_PATH = "datas/btc_4h_full.csv"

engine = RiskEngine(RiskConfig(), MODEL_PATH)
state_manager = StateManager()

app = FastAPI()


# ---- load or initialize state ----

states = state_manager.load_all()

for symbol in SYMBOLS:

    if symbol not in states:

        df = pd.read_csv(DATA_PATH)
        states[symbol] = engine.initialize_state(df)

state_manager.save_all(states)


# ---- endpoints ----

@app.get("/")
def health():
    return {"status": "running"}


@app.get("/signal")
def get_signal():
    return state


@app.get("/signal/{symbol}")
def get_signal_symbol(symbol: str):

    if symbol not in states:
        return {"error": "symbol not supported"}

    return states[symbol]


@app.post("/update")
def update_signal(candle: dict):

    global state

    result, state = engine.update_with_new_candle(state, candle)

    state_manager.save_state(state)

    return result

def scheduled_update():

    global states

    for symbol in SYMBOLS:

        candle = get_latest_candle(symbol)

        result, states[symbol] = engine.update_with_new_candle(
            states[symbol],
            candle
        )

        print(symbol, result)

    state_manager.save_all(states)


# ---- scheduler ----

scheduler = BackgroundScheduler()

scheduler.add_job(
    scheduled_update,
    "interval",
    hours=4
)

scheduler.start()