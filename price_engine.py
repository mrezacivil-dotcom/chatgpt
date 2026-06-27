import requests

BASE = "https://api.binance.com/api/v3"

def get_price(symbol):
    try:
        r = requests.get(f"{BASE}/ticker/price?symbol={symbol}", timeout=5)
        return float(r.json()["price"])
    except Exception:
        return None

def get_klines(symbol, interval="1h", limit=250):
    """
    حالا علاوه بر قیمت بسته شدن، بالاترین و پایین ترین قیمت را هم برمی‌گرداند
    """
    try:
        r = requests.get(
            f"{BASE}/klines?symbol={symbol}&interval={interval}&limit={limit}",
            timeout=8
        )
        data = r.json()
        return {
            "closes": [float(c[4]) for c in data],
            "highs": [float(c[2]) for c in data],
            "lows": [float(c[3]) for c in data]
        }
    except Exception:
        return {"closes": [], "highs": [], "lows": []}
