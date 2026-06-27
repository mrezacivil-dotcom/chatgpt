import time
from signal_engine import get_signals
from execution_engine import open_position, update_positions, get_positions, has_position
from price_engine import get_price
from telegram_engine import send_signal
from risk_engine import trading_allowed

TRADE_LOCK = {}
LOCK_SECONDS = 60

def set_trade_lock(symbol):
    """قفل می‌کند بعد از ترید"""
    TRADE_LOCK[symbol] = time.time()

def is_trade_locked(symbol):
    """چک می‌کند اگر قفل هنوز پابرجاست"""
    if symbol in TRADE_LOCK:
        if time.time() - TRADE_LOCK[symbol] < LOCK_SECONDS:
            return True
        else:
            del TRADE_LOCK[symbol] # قفل منقضی شده را پاک می‌کند
    return False

def run():
    print("🚀 V65 SYSTEM STARTED")
    while True:
        try:
            print("🔁 LOOP RUNNING")
            update_positions(get_price)

            if not trading_allowed():
                print("⚠️ TRADING DISABLED (Risk Limits)")
                time.sleep(5)
                continue

            signals = get_signals()
            if not signals:
                print("📡 NO SIGNAL")
                time.sleep(2)
                continue

            best = max(signals, key=lambda x: x["score"])
            print("🔥 BEST SIGNAL:", best['symbol'], best['direction'])

            symbol = best.get("symbol")

            if is_trade_locked(symbol):
                print(f"⛔ TRADE LOCKED for {symbol}")
                time.sleep(2)
                continue

            if has_position(symbol):
                print(f"⛔ POSITION EXISTS for {symbol}")
                time.sleep(2)
                continue

            pos = open_position(best)
            if pos:
                send_signal(best)
                set_trade_lock(symbol) # قفل کردن ارز پس از ترید موفق

            print("📊 OPEN POSITIONS:", len(get_positions()))
            time.sleep(2)

        except Exception as e:
            print("❌ SYSTEM ERROR:", repr(e))
            time.sleep(3)

if __name__ == "__main__":
    run()
