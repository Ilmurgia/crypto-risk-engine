import requests
import pandas as pd
import time

symbol = "ETHUSDT"
interval = "4h"
limit = 1000

url = "https://api.binance.com/api/v3/klines"

all_data = []
start_time = 1502942400000  # 2017-08-17

while True:
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": start_time
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data:
        break
    
    all_data.extend(data)
    start_time = data[-1][0] + 1
    
    print("Scaricate:", len(all_data))
    
    time.sleep(0.5)

df = pd.DataFrame(all_data, columns=[
    "timestamp","open","high","low","close","volume",
    "close_time","qav","num_trades","taker_base","taker_quote","ignore"
])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

for col in ["open","high","low","close","volume"]:
    df[col] = df[col].astype(float)

df = df[["timestamp","open","high","low","close","volume"]]

df.to_csv("datas/eth_4h.csv", index=False)

print("Download completato.")