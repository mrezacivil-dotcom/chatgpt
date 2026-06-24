import time

from signal_engine import get_signals
from execution_engine import (
    open_position,
    update_positions,
    get_positions,
    has_position
)
from price_engine import get_price
from telegram_engine import send_signal
from risk_engine import trading_allowed


TRADE_LOCK = {}
LOCK_SECONDS = 60


def is_trade_locked(symbol):
    now = time.time()

    if symbol in TRADE_LOCK:
        if now - TRADE_LOCK[symbol] < LOCK_SECONDS:
            return True

    TRADE_LOCK[symbol] = now
    return False


def run():
    print("🚀 V64 SYSTEM STARTED")

    while True:
        try:
            # آپدیت پوزیشن‌ها
            update_positions(get_price)

            # چک ریسک
            if not trading_allowed():
                time.sleep(5)
                continue

            # گرفتن سیگنال
            signals = get_signals()

            if not signals:
                print("📡 NO SIGNAL")
                time.sleep(2)
                continue

            best = max(signals, key=lambda x: x["score"])
            print("🔥 SIGNAL:", best)

            symbol = best.get("symbol")

            if not symbol:
                print("⚠️ INVALID SIGNAL (NO SYMBOL)")
                time.sleep(2)
                continue

            if is_trade_locked(symbol):
                print("⛔ TRADE LOCKED")
                time.sleep(2)
                continue

            if has_position(symbol):
                print("⛔ POSITION EXISTS")
                time.sleep(2)
                continue

            pos = open_position(best)

            if pos:
                send_signal(best)

            print("📊 POSITIONS:", len(get_positions()))

            time.sleep(2)

        except Exception as e:
            print("❌ ERROR:", str(e))
            time.sleep(3)


if __name__ == "__main__":
    run()
