import time
import json
import os

from signal_engine import get_signals
from execution_engine import (
    open_position,
    update_positions,
    get_positions,
    has_position
)
from price_engine import get_price
from telegram_engine import send_signal


LOCK_FILE = "trade_lock.json"
LOCK_SECONDS = 60


def load_lock():
    if not os.path.exists(LOCK_FILE):
        return {}
    try:
        with open(LOCK_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_lock(data):
    with open(LOCK_FILE, "w") as f:
        json.dump(data, f)


def is_trade_locked(symbol, direction):
    key = f"{symbol}_{direction}"
    now = time.time()

    lock = load_lock()

    if key in lock:
        if now - lock[key] < LOCK_SECONDS:
            return True

    lock[key] = now
    save_lock(lock)
    return False


def run():
    print("🚀 GITHUB SIGNAL BOT STARTED")

    try:
        update_positions(get_price)

        signals = get_signals()

        if not signals:
            print("📡 NO SIGNAL")
            return

        best = max(signals, key=lambda x: x["score"])
        print("🔥 SIGNAL:", best)

        symbol = best["symbol"]
        direction = best["direction"]

        if is_trade_locked(symbol, direction):
            print("⛔ LOCKED")
            return

        if has_position(symbol, direction):
            print("⛔ POSITION EXISTS")
            return

        open_position(best)
        send_signal(best)

        print("📊 TOTAL POSITIONS:", len(get_positions()))

    except Exception as e:
        print("❌ ERROR:", e)


if __name__ == "__main__":
    run()
send_signal({
    "symbol": "TEST",
    "direction": "LONG",
    "score": 100
})
