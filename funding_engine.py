from price_engine import get_funding_rate


def get_funding_bias(symbol):
    """دریافت بایاس فاندینگ واقعی"""
    rate = get_funding_rate(symbol)

    if rate > 0.001:
        return "OVERLONG", rate
    elif rate < -0.001:
        return "OVERSHORT", rate
    else:
        return "NEUTRAL", rate


def funding_filter(direction, symbol):
    """فیلتر فاندینگ ریت"""
    bias, rate = get_funding_bias(symbol)

    # اگر فاندینگ خیلی مثبته، خرید خطرناکه
    if bias == "OVERLONG" and direction == "BUY":
        print(f"⚠️ FUNDING FILTER: {symbol} overlong ({rate:.4f})")
        return False

    # اگر فاندینگ خیلی منفیه، فروش خطرناکه
    if bias == "OVERSHORT" and direction == "SELL":
        print(f"⚠️ FUNDING FILTER: {symbol} overshort ({rate:.4f})")
        return False

    return True
