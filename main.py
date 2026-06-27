import time

from signal_engine import get_signals
from execution_engine import (
    open_position, update_positions,
    get_positions, has_position
)
from price_engine import get_price
from telegram_engine import send_signal, send_alert
from risk_engine import trading_allowed, get_account_stats
from config import SLEEP_TIME, MAX_POSITIONS


TRADE_LOCK = {}
LOCK_SECONDS = 60


def is_trade_locked(symbol):
    """قفل ترید برای جلوگیری از ترید تکراری"""
    now = time.time()

    if symbol in TRADE_LOCK:
        if now - TRADE_LOCK[symbol] < LOCK_SECONDS:
            return True

    TRADE_LOCK[symbol] = now
    return False


def print_status():
    """نمایش وضعیت"""
    stats = get_account_stats()
    positions = get_positions()

    print(f"\n{'='*40}")
    print(f"💰 Balance: ${stats['balance']}")
    print(f"📊 Trades: {stats['total_trades']} | WR: {stats['winrate']}%")
    print(f"📉 Max DD: {stats['max_drawdown']}%")
    print(f"📂 Open Positions: {len(positions)}/{MAX_POSITIONS}")
    print(f"{'='*40}\n")


def run():
    """حلقه اصلی ربات"""

    print("=" * 50)
    print("🚀 V65 PRO TRADING SYSTEM")
    print("=" * 50)

    loop_count = 0

    while True:
        try:
            loop_count += 1

            # هر ۲۰ لوپ وضعیت نشان بده
            if loop_count % 20 == 0:
                print_status()

            # بروزرسانی پوزیشن‌ها
            closed = update_positions(get_price)

            if closed:
                for pos in closed:
                    emoji = "🎯" if pos["result"] == "WIN" else "🔴"
                    print(f"{emoji} CLOSED: {pos['symbol']} "
                          f"{pos['result']} ({pos['profit']:.4f})")

            # بررسی مجوز ترید
            if not trading_allowed():
                print("⚠️ TRADING PAUSED")
                time.sleep(SLEEP_TIME * 2)
                continue

            # دریافت سیگنال‌ها
            signals = get_signals()

            if not signals:
                time.sleep(SLEEP_TIME)
                continue

            # بهترین سیگنال
            best = signals[0]  # قبلاً مرتب شده

            print(f"\n🔥 SIGNAL: {best['symbol']} {best['direction']}")
            print(f"   Score: {best['score']} | Conf: {best['confidence']}%")
            print(f"   Reasons: {', '.join(best.get('reasons', []))}")

            symbol = best["symbol"]

            # بررسی قفل‌ها
            if is_trade_locked(symbol):
                print("⏳ TRADE LOCKED")
                time.sleep(SLEEP_TIME)
                continue

            if has_position(symbol):
                print("📂 POSITION EXISTS")
                time.sleep(SLEEP_TIME)
                continue

            if len(get_positions()) >= MAX_POSITIONS:
                print(f"⛔ MAX POSITIONS ({MAX_POSITIONS})")
                time.sleep(SLEEP_TIME)
                continue

            # باز کردن پوزیشن
            pos = open_position(best)

            if pos:
                send_signal(best)
                print("✅ POSITION OPENED & SIGNAL SENT")

            time.sleep(SLEEP_TIME)

        except KeyboardInterrupt:
            print("\n⚠️ SHUTTING DOWN...")
            send_alert("Bot stopped by user")
            break

        except Exception as e:
            print(f"❌ ERROR: {repr(e)}")
            time.sleep(SLEEP_TIME * 2)


if __name__ == "__main__":
    run()
