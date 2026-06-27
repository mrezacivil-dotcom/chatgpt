import requests
import time
import random
from config import CACHE_SECONDS

# ============================================
# 🌐 تنظیمات اصلی
# ============================================
BASE_SPOT = "https://api.binance.com/api/v3"
BASE_FUTURES = "https://fapi.binance.com/fapi/v1"

# هدرهای ضروری برای دور زدن 451
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.binance.com/",
    "Origin": "https://www.binance.com"
}

# اگر VPN یا پراکسی دارید اینجا وارد کنید (اختیاری)
PROXIES = {
    # "http": "http://user:pass@ip:port",
    # "https": "http://user:pass@ip:port"
}

# کش داده‌ها
_price_cache = {}
_kline_cache = {}
_last_request_time = 0
MIN_REQUEST_INTERVAL = 0.1  # فاصله بین درخواست‌ها


def _rate_limit():
    """کنترل سرعت درخواست"""
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.time()


def _safe_request(url, params=None, max_retries=3):
    """درخواست امن با ریترای"""
    for attempt in range(max_retries):
        try:
            _rate_limit()
            
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                proxies=PROXIES if PROXIES else None,
                timeout=10
            )
            
            # اگر 451 یا 403 داد، یکم صبر کن و دوباره امتحان کن
            if response.status_code in [451, 403, 418]:
                wait_time = (attempt + 1) * 2 + random.uniform(0, 1)
                print(f"⚠️ Error {response.status_code}, retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1 + attempt)
    
    return None


def get_price(symbol):
    """دریافت قیمت لحظه‌ای"""
    now = time.time()
    
    if symbol in _price_cache:
        cached_time, cached_price = _price_cache[symbol]
        if now - cached_time < CACHE_SECONDS:
            return cached_price

    try:
        # تلاش با API اسپات
        data = _safe_request(f"{BASE_SPOT}/ticker/price", {"symbol": symbol})
        
        if data and "price" in data:
            price = float(data["price"])
            _price_cache[symbol] = (now, price)
            return price
            
    except Exception as e:
        print(f"⚠️ Spot Price Error {symbol}: {e}")
        
        # تلاش با API فیوچرز اگر اسپات fail شد
        try:
            data = _safe_request(f"{BASE_FUTURES}/ticker/price", {"symbol": symbol})
            if data and "price" in data:
                price = float(data["price"])
                _price_cache[symbol] = (now, price)
                print(f"✅ {symbol} price from Futures API")
                return price
        except:
            pass

    # اگر کش قدیمی داریم برگردان
    if symbol in _price_cache:
        print(f"⚠️ Using cached price for {symbol}")
        return _price_cache[symbol][1]
        
    return None


def get_klines(symbol, interval="1h", limit=200):
    """دریافت کندل‌ها با fallback به فیوچرز"""
    now = time.time()
    cache_key = f"{symbol}_{interval}"

    if cache_key in _kline_cache:
        cached_time, cached_data = _kline_cache[cache_key]
        if now - cached_time < CACHE_SECONDS * 10:
            return cached_data

    try:
        # تلاش با اسپات
        data = _safe_request(
            f"{BASE_SPOT}/klines",
            {"symbol": symbol, "interval": interval, "limit": limit}
        )
        
        if not data:
            raise Exception("Empty response")
            
    except Exception as e:
        print(f"⚠️ Spot Klines failed for {symbol}, trying Futures...")
        
        try:
            # تلاش با فیوچرز (گاهی اوقات محدودیت متفاوتی دارد)
            data = _safe_request(
                f"{BASE_FUTURES}/klines",
                {"symbol": symbol, "interval": interval, "limit": limit}
            )
            
            if not data:
                raise Exception("Futures also failed")
                
            print(f"✅ {symbol} klines from Futures API")
            
        except Exception as e2:
            print(f"❌ Both Spot and Futures failed for {symbol}")
            # اگر کش قدیمی داریم برگردان
            if cache_key in _kline_cache:
                return _kline_cache[cache_key][1]
            return {"closes": [], "highs": [], "lows": [], "volumes": []}

    try:
        # پردازش داده‌ها
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
        
    except Exception as e:
        print(f"❌ Parse error for {symbol}: {e}")
        if cache_key in _kline_cache:
            return _kline_cache[cache_key][1]
        return {"closes": [], "highs": [], "lows": [], "volumes": []}


def get_funding_rate(symbol):
    """دریافت فاندینگ ریت (فقط فیوچرز)"""
    try:
        data = _safe_request(
            f"{BASE_FUTURES}/fundingRate",
            {"symbol": symbol, "limit": 1}
        )
        
        if data and len(data) > 0:
            return float(data[0]["fundingRate"])
            
    except Exception as e:
        print(f"⚠️ Funding rate error {symbol}: {e}")
    
    return 0.0


def test_connection():
    """تست اتصال به بایننس"""
    print("🌐 Testing Binance connection...")
    try:
        # تست پینگ
        data = _safe_request(f"{BASE_SPOT}/ping")
        if data == {}:
            print("✅ Spot API: OK")
        else:
            print("⚠️ Spot API: Unexpected response")
            
        # تست سرور زمان
        data = _safe_request(f"{BASE_SPOT}/time")
        if data and "serverTime" in data:
            print(f"✅ Server time: {data['serverTime']}")
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("💡 Tips:")
        print("   1. Check your internet connection")
        print("   2. Try using a VPN (Binance blocks some countries)")
        print("   3. Check if Binance is accessible in your region")
