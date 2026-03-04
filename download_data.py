import requests
import pandas as pd
import time
from datetime import datetime

symbol = "BTCUSDT"
interval = "4h"
limit = 1000
base_url = "https://api.binance.com/api/v3/klines"

start_str = "1 Jan 2017"
start_time = int(datetime.strptime(start_str, "%d %b %Y").timestamp() * 1000)

all_data = []

print("Download iniziato...")

while True:
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": start_time
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if not data:
        break

    all_data.extend(data)

    start_time = data[-1][0] + 1

    print("Scaricate:", len(all_data))

    time.sleep(0.5)

    if len(data) < limit:
        break

print("Download completato.")

columns = [
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
]

df = pd.DataFrame(all_data, columns=columns)

df = df[["timestamp", "open", "high", "low", "close", "volume"]]

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df.astype({
    "open": float,
    "high": float,
    "low": float,
    "close": float,
    "volume": float
})

df = df.drop_duplicates()

df.to_csv("datas/btc_4h_full.csv", index=False)

print("Righe totali:", len(df))
print("Da:", df["timestamp"].min())
print("A:", df["timestamp"].max())