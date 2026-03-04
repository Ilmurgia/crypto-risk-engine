import requests


def get_latest_candle():

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": "BTCUSDT",
        "interval": "4h",
        "limit": 1
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()[0]

    return {
        "open": float(data[1]),
        "high": float(data[2]),
        "low": float(data[3]),
        "close": float(data[4])
    }