import pandas as pd
import numpy as np


def compute_indicators(
    df: pd.DataFrame,
    atr_window: int,
    ema_window: int
) -> pd.DataFrame:

    df = df.copy()

    # True Range
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift(1))
    low_close = np.abs(df["low"] - df["close"].shift(1))

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    df["atr"] = tr.rolling(atr_window).mean()

    # EMA
    df["ema"] = df["close"].ewm(span=ema_window, adjust=False).mean()

    return df