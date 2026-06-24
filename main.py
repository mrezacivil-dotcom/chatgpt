import time
from signal_engine import get_signals
from execution_engine import open_position
from risk_engine import trading_allowed
from telegram_engine import send_signal

TRADE_LOCK = {}
LOCK_SECONDS = 60

def is_locked(symbol):
    now = time.time()
    if symbol in TRADE_LOCK and now - TRADE_LOCK[symbol] < LOCK_SECONDS:
        return True
    TRADE_LOCK[symbol] = now
    return False

def run():
    print("🚀 BOT STARTED")
    while True:
        signals = get_signals()

        for s in signals:
            if is_locked(s["symbol"]):
                continue

            if not trading_allowed(s):
                continue

            open_position(s)
            send_signal(s)

        time.sleep(5)

if __name__ == "__main__":
    run()
