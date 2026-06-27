import requests
import time
from config import CACHE_SECONDS

BASE = "https://api.binance.com/api/v3"

# کش قیمت‌ها برای جلوگیری از درخواست زیاد
_price_cache = {}
_kline_cache = {}


def get_price(symbol):
    """دریافت قیمت لحظه‌ای با کش"""
    now = time.time()

    if symbol in _price_cache:
        cached_time, cached_price = _price_cache[symbol]
        if now - cached_time < CACHE_SECONDS:
            return cached_price

    try:
        r = requests.get(
            f"{BASE}/ticker/price",
            params={"symbol": symbol},
            timeout=5
        )
        r.raise_for_status()
        price = float(r.json()["price"])
        _price_cache[symbol] = (now, price)
        return price

    except requests.RequestException as e:
        print(f"⚠️ PRICE ERROR {symbol}: {e}")
        # اگر کش قدیمی داریم برگردان
        if symbol in _price_cache:
            return _price_cache[symbol][1]
        return None


def get_klines(symbol, interval="1h", limit=200):
    """دریافت کندل‌ها با کش"""
    now = time.time()
    cache_key = f"{symbol}_{interval}"

    if cache_key in _kline_cache:
        cached_time, cached_data = _kline_cache[cache_key]
        if now - cached_time < CACHE_SECONDS * 10:
            return cached_data

    try:
        r = requests.get(
            f"{BASE}/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            },
            timeout=8
        )
        r.raise_for_status()

        closes = [float(c[4]) for c in r.json()]
        highs = [float(c[2]) for c in r.json()]
        lows = [float(c[3]) for c in r.json()]
        volumes = [float(c[5]) for c in r.json()]

        result = {
            "closes": closes,
            "highs": highs,
            "lows": lows,
            "volumes": volumes
        }

        _kline_cache[cache_key] = (now, result)
        return result

    except requests.RequestException as e:
        print(f"⚠️ KLINE ERROR {symbol}: {e}")
        if cache_key in _kline_cache:
            return _kline_cache[cache_key][1]
        return {"closes": [], "highs": [], "lows": [], "volumes": []}


def get_funding_rate(symbol):
    """دریافت فاندینگ ریت واقعی"""
    try:
        r = requests.get(
            "https://fapi.binance.com/fapi/v1/fundingRate",
            params={"symbol": symbol, "limit": 1},
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        if data:
            return float(data[0]["fundingRate"])
    except Exception as e:
        print(f"⚠️ FUNDING ERROR {symbol}: {e}")

    return 0.0
