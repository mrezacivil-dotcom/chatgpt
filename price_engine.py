import requests

BASE = "https://api.binance.com/api/v3"


def get_price(symbol):
    try:
        r = requests.get(f"{BASE}/ticker/price?symbol={symbol}", timeout=5)
        return float(r.json()["price"])
    except:
        return None


def get_klines(symbol, interval="1h", limit=200):
    try:
        r = requests.get(
            f"{BASE}/klines?symbol={symbol}&interval={interval}&limit={limit}",
            timeout=8
        )
        return [float(c[4]) for c in r.json()]
    except:
        return []
