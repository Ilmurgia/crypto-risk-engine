from dataclasses import dataclass


@dataclass
class EngineState:
    ema: float
    atr: float
    prev_close: float