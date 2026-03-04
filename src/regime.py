import pandas as pd


def compute_regime(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    if "ema" not in df.columns:
        raise ValueError("EMA column not found. Run indicators first.")

    df["regime"] = (df["close"] > df["ema"]).astype(int)

    return df