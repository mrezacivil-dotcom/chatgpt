# لیست ارزهای با ریسک بالا
HIGH_RISK_SYMBOLS = ["WLDUSDT", "SUIUSDT"]

# لیست ارزهای قوی
STRONG_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]


def fundamental_filter(symbol, direction):
    """فیلتر فاندامنتال"""

    # ارزهای پر ریسک - فقط با اسکور بالا ترید کن
    if symbol in HIGH_RISK_SYMBOLS:
        return True  # اجازه بده ولی اسکور تنظیم میشه

    return True


def fundamental_score_adjust(symbol, base_score):
    """تنظیم اسکور بر اساس فاندامنتال"""

    if symbol in STRONG_SYMBOLS:
        return base_score * 1.1

    if symbol in HIGH_RISK_SYMBOLS:
        return base_score * 0.9

    return base_score
