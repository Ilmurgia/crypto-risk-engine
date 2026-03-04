import pandas as pd
import numpy as np
from dataclasses import dataclass

from .indicators import compute_indicators
from .regime import compute_regime
from .tail_model import TailModel


@dataclass
class RiskConfig:
    atr_window: int = 14
    ema_window: int = 200
    max_exposure: float = 1.0
    min_exposure: float = 0.0


class RiskEngine:

    def __init__(self, config: RiskConfig, model_path: str):
        self.config = config
        self.tail_model = TailModel(model_path)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Indicators
        df = compute_indicators(
            df,
            self.config.atr_window,
            self.config.ema_window
        )

        # Regime
        df = compute_regime(df)

        # Tail probability (only last row inference)
        df["tail_prob"] = np.nan

        last_row = df.iloc[-1:].copy()
        prob = self.tail_model.predict_proba(last_row)

        df.iloc[-1, df.columns.get_loc("tail_prob")] = prob

        # Exposure
        df["exposure"] = self._compute_exposure(df)

        return df

    def _compute_exposure(self, df: pd.DataFrame) -> pd.Series:

        scaled = self.config.max_exposure * (1 - df["tail_prob"])

        scaled = np.where(
            df["regime"] == 1,
            scaled,
            self.config.min_exposure
        )

        scaled = np.clip(
            scaled,
            self.config.min_exposure,
            self.config.max_exposure
        )

        return pd.Series(scaled, index=df.index)
    
    def initialize_state(self, df: pd.DataFrame):

        df = compute_indicators(
        df,
        self.config.atr_window,
        self.config.ema_window
        )

        last = df.iloc[-1]

        if pd.isna(last["atr"]) or pd.isna(last["ema"]):
            raise ValueError("Not enough data to initialize state")

        return {
        "ema": last["ema"],
        "atr": last["atr"],
        "prev_close": last["close"]
        }      
    
    def update_with_new_candle(self, state: dict, new_row: dict):

        close = new_row["close"]
        high = new_row["high"]
        low = new_row["low"]

        # === EMA update ===
        k = 2 / (self.config.ema_window + 1)
        ema = close * k + state["ema"] * (1 - k)

        # === ATR update ===
        tr = max(
            high - low,
            abs(high - state["prev_close"]),
            abs(low - state["prev_close"])
        )

        atr = (state["atr"] * (self.config.atr_window - 1) + tr) / self.config.atr_window

        regime = int(close > ema)

        # Predict tail prob
        df_temp = pd.DataFrame([{"atr": atr}])

        tail_prob = self.tail_model.predict_proba(df_temp)

        if pd.isna(tail_prob):
            exposure = self.config.min_exposure
        else:
            exposure = self.config.max_exposure * (1 - tail_prob)

        if regime == 0:
            exposure = self.config.min_exposure

        exposure = max(self.config.min_exposure,
                       min(self.config.max_exposure, exposure))

        new_state = {
            "ema": ema,
            "atr": atr,
            "prev_close": close
        }

        return {
            "tail_prob": tail_prob,
            "regime": regime,
            "exposure": exposure
        }, new_state