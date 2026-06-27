import time
from config import MAX_POSITIONS

positions = []


def open_position(signal):
    """باز کردن پوزیشن جدید"""

    if len(positions) >= MAX_POSITIONS:
        print(f"⛔ MAX POSITIONS ({MAX_POSITIONS})")
        return None

    position = {
        "id": int(time.time() * 1000),
        "symbol": signal["symbol"],
        "direction": signal["direction"],
        "entry": signal["entry"],
        "sl": signal["sl"],
        "tp": signal["tp"],
        "score": signal["score"],
        "confidence": signal["confidence"],
        "open_time": time.time(),
        "status": "OPEN"
    }

    positions.append(position)

    print(f"✅ OPENED {signal['direction']} {signal['symbol']}")
    print(f"   Entry: {signal['entry']:.4f}")
    print(f"   SL: {signal['sl']:.4f} | TP: {signal['tp']:.4f}")

    return position


def update_positions(get_price_func):
    """بررسی و بروزرسانی پوزیشن‌ها"""
    from risk_engine import update_account
    from ai_core import update_memory

    closed = []

    for pos in positions:
        if pos["status"] != "OPEN":
            continue

        current_price = get_price_func(pos["symbol"])

        if current_price is None:
            continue

        result = None
        profit = 0.0

        if pos["direction"] == "BUY":
            # بررسی TP
            if current_price >= pos["tp"]:
                profit = pos["tp"] - pos["entry"]
                result = "WIN"
                print(f"🎯 TP HIT {pos['symbol']} +{profit:.4f}")

            # بررسی SL
            elif current_price <= pos["sl"]:
                profit = pos["entry"] - pos["sl"]
                result = "LOSS"
                print(f"🔴 SL HIT {pos['symbol']} -{profit:.4f}")

        elif pos["direction"] == "SELL":
            # بررسی TP
            if current_price <= pos["tp"]:
                profit = pos["entry"] - pos["tp"]
                result = "WIN"
                print(f"🎯 TP HIT {pos['symbol']} +{profit:.4f}")

            # بررسی SL
            elif current_price >= pos["sl"]:
                profit = pos["sl"] - pos["entry"]
                result = "LOSS"
                print(f"🔴 SL HIT {pos['symbol']} -{profit:.4f}")

        if result:
            pos["status"] = "CLOSED"
            pos["result"] = result
            pos["profit"] = profit
            pos["close_time"] = time.time()

            update_account(result, profit)
            update_memory(pos["symbol"], result, profit)
            closed.append(pos)

    # حذف پوزیشن‌های بسته شده
    for pos in closed:
        if pos in positions:
            positions.remove(pos)

    return closed


def has_position(symbol):
    """آیا پوزیشن باز داریم؟"""
    return any(
        p["symbol"] == symbol and p["status"] == "OPEN"
        for p in positions
    )


def get_positions():
    """لیست پوزیشن‌های باز"""
    return [p for p in positions if p["status"] == "OPEN"]


def close_all_positions():
    """بستن همه پوزیشن‌ها"""
    for pos in positions:
        pos["status"] = "CLOSED"
    positions.clear()
    print("⚠️ ALL POSITIONS CLOSED")
