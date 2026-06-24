import requests

BASE = "https://api.binance.com/api/v3"


def get_price(symbol):
    try:
        r = requests.get(
            f"{BASE}/ticker/price?symbol={symbol}",
            timeout=5
        )

        r.raise_for_status()

        return float(r.json()["price"])

    except Exception as e:
        print("PRICE ERROR:", symbol, e)
        return None


def get_klines(symbol, interval="1h", limit=200):

    try:

        r = requests.get(
            f"{BASE}/klines?symbol={symbol}&interval={interval}&limit={limit}",
            timeout=8
        )

        r.raise_for_status()

        data = r.json()

        return [float(c[4]) for c in data]

    except Exception as e:

        print("KLINES ERROR:", symbol, e)
        return []


def get_ohlcv(symbol, interval="1h", limit=200):

    try:

        r = requests.get(
            f"{BASE}/klines?symbol={symbol}&interval={interval}&limit={limit}",
            timeout=8
        )

        r.raise_for_status()

        data = r.json()

        return {
            "close": [float(c[4]) for c in data],
            "high": [float(c[2]) for c in data],
            "low": [float(c[3]) for c in data],
            "volume": [float(c[5]) for c in data]
        }

    except Exception as e:

        print("OHLCV ERROR:", symbol, e)

        return {
            "close": [],
            "high": [],
            "low": [],
            "volume": []
        }
