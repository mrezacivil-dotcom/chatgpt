import requests
import time
from config import CACHE_SECONDS

# ============================================
# 🌍 تنظیمات اتصال
# ============================================
# اگر از ایران یا آمریکا هستید و ارور 451 گرفتید، 
# آدرس‌های زیر را یکی یکی تست کنید:

BASE_URLS = [
    "https://api.binance.com/api/v3",          # آدرس اصلی
    "https://api1.binance.com/api/v3",         # آدرس جایگزین ۱
    "https://api2.binance.com/api/v3",         # آدرس جایگزین ۲
    "https://api3.binance.com/api/v3",         # آدرس جایگزین ۳
    "https://api4.binance.com/api/v3",         # آدرس جایگزین ۴
    # "https://api.binance.us/api/v3",         # اگر در آمریکا هستید این را فعال کنید
]

FUTURES_BASE = "https://fapi.binance.com/fapi/v1"

# کش قیمت‌ها
_price_cache = {}
_kline_cache = {}

# ============================================
# 🕵️ ساخت سشن هوشمند (شبیه‌سازی مرورگر)
# ============================================
session = requests.Session()

# این هدرها بسیار مهم هستند تا بایننس ما را به عنوان ربات مسدود نکند
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json,text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
})


def get_working_base():
    """پیدا کردن آدرس سالم بایننس"""
    for base in BASE_URLS:
        try:
            r = session.get(f"{base}/ping", timeout=3)
            if r.status_code == 200:
                print(f"✅ BINANCE CONNECTED: {base}")
                return base
        except:
            continue
    
    print("❌ ALL BINANCE URLS FAILED!")
    return BASE_URLS[0]


# پیدا کردن بهترین آدرس هنگام شروع
BASE = get_working_base()


def get_price(symbol):
    """دریافت قیمت لحظه‌ای با کش"""
    now = time.time()

    if symbol in _price_cache:
        cached_time, cached_price = _price_cache[symbol]
        if now - cached_time < CACHE_SECONDS:
            return cached_price

    try:
        r = session.get(
            f"{BASE}/ticker/price",
            params={"symbol": symbol},
            timeout=5
        )
        
        if r.status_code == 451:
            print(f"⛔ 451 ERROR for {symbol} - IP BLOCKED!")
            return _price_cache.get(symbol, (0, None))[1]
            
        r.raise_for_status()
        price = float(r.json()["price"])
        _price_cache[symbol] = (now, price)
        return price

    except Exception as e:
        print(f"⚠️ PRICE ERROR {symbol}: {e}")
        if symbol in _price_cache:
            return _price_cache[symbol][1]
        return None


def get_klines(symbol, interval="1h", limit=200):
    """دریافت کندل‌ها با کش و مدیریت خطا"""
    now = time.time()
    cache_key = f"{symbol}_{interval}"

    if cache_key in _kline_cache:
        cached_time, cached_data = _kline_cache[cache_key]
        if now - cached_time < CACHE_SECONDS * 10:
            return cached_data

    try:
        r = session.get(
            f"{BASE}/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            },
            timeout=10
        )
        
        # مدیریت خطای 451
        if r.status_code == 451:
            print(f"⛔ 451 ERROR for {symbol} - IP BLOCKED! Trying alternate URL...")
            # تلاش با آدرس جایگزین
            for alt_base in BASE_URLS:
                try:
                    r2 = session.get(
                        f"{alt_base}/klines",
                        params={"symbol": symbol, "interval": interval, "limit": limit},
                        timeout=10
                    )
                    if r2.status_code == 200:
                        return parse_kline_data(r2.json(), cache_key, now)
                except:
                    continue
            return {"closes": [], "highs": [], "lows": [], "volumes": []}
        
        r.raise_for_status()
        return parse_kline_data(r.json(), cache_key, now)

    except Exception as e:
        print(f"⚠️ KLINE ERROR {symbol}: {e}")
        if cache_key in _kline_cache:
            return _kline_cache[cache_key][1]
        return {"closes": [], "highs": [], "lows": [], "volumes": []}


def parse_kline_data(data, cache_key, now):
    """پردازش داده‌های کندل"""
    closes = [float(c[4]) for c in data]
    highs = [float(c[2]) for c in data]
    lows = [float(c[3]) for c in data]
    volumes = [float(c[5]) for c in data]

    result = {
        "closes": closes,
        "highs": highs,
        "lows": lows,
        "volumes": volumes
    }

    _kline_cache[cache_key] = (now, result)
    return result


def get_funding_rate(symbol):
    """دریافت فاندینگ ریت واقعی"""
    try:
        r = session.get(
            f"{FUTURES_BASE}/fundingRate",
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
