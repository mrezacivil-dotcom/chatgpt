import requests

def get_funding_bias(symbol):
    try:
        # سمبول‌های اسپات USDT هستند، برای فیوچرز USDT اضافه میشه
        fut_symbol = symbol if symbol.endswith("USDT") else symbol + "USDT"
        r = requests.get(f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={fut_symbol}", timeout=3)
        rate = float(r.json().get("lastFundingRate", 0))
        
        if rate > 0.0005: return "OVERLONG"  # فاندینگ بالا یعنی لانگ‌ها بیش از حد
        if rate < -0.0005: return "OVERSHORT" # فاندینگ منفی شدید یعنی شورت‌ها بیش از حد
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def funding_filter(direction, bias):
    # اگر مارکت اورلانگ است، سیگنال خرید ندهید (ریسک لیکویید شدن لانگ‌ها بالاست)
    if bias == "OVERLONG" and direction == "BUY":
        return False
    # اگر مارکت اورشورت است، سیگنال فروش ندهید
    if bias == "OVERSHORT" and direction == "SELL":
        return False
    return True
