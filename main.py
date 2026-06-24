import time
from telegram_engine import send_signal

# اگر این ماژول‌ها وجود دارند
from signal_engine import get_signals
from execution_engine import open_position
from risk_engine import trading_allowed

TRADE_LOCK = {}
LOCK_SECONDS = 60


def is_locked(symbol):
    now = time.time()

    if symbol in TRADE_LOCK:
        if now - TRADE_LOCK[symbol] < LOCK_SECONDS:
            return True

    TRADE_LOCK[symbol] = now
    return False


def test_telegram():
    print("TESTING TELEGRAM...")

    test_signal = {
        "symbol": "BTCUSDT",
        "direction": "LONG",
        "entry": 100000,
        "sl": 99000,
        "tp": 102000,
        "score": 10,
        "confidence": "100%"
    }

    send_signal(test_signal)

    print("TEST MESSAGE SENT")


def run():

    print("🚀 BOT STARTED")

    # تست تلگرام هنگام استارت
    test_telegram()

    while True:

        try:

            print("SCAN STARTED")

            signals = get_signals()

            print(f"SIGNALS FOUND: {len(signals)}")
            print(signals)

            for s in signals:

                symbol = s.get("symbol", "UNKNOWN")

                print(f"CHECKING {symbol}")

                if is_locked(symbol):
                    print(f"LOCKED: {symbol}")
                    continue

                if not trading_allowed(s):
                    print(f"RISK FILTER BLOCKED: {symbol}")
                    continue

                print(f"OPENING POSITION: {symbol}")

                open_position(s)

                print(f"SENDING TELEGRAM: {symbol}")

                send_signal(s)

                print(f"DONE: {symbol}")

        except Exception as e:
            print("ERROR:", str(e))

        time.sleep(5)


if __name__ == "__main__":
    run()
