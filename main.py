import time

from signal_engine import get_signals
from execution_engine import (
    open_position,
    update_positions,
    has_position
)
from price_engine import get_price
from telegram_engine import send_signal


def run():

    print("🚀 GITHUB SIGNAL BOT STARTED")

    while True:

        try:
            print("STEP 1: update_positions")
            update_positions(get_price)

            print("STEP 2: get_signals")
            signals = get_signals()

            print("SIGNALS RAW:", signals)

            if not signals:
                print("📡 NO SIGNAL")
                time.sleep(2)
                continue

            print("STEP 3: select best signal")

            best = max(signals, key=lambda x: x["score"])

            print("🔥 SIGNAL:", best)

            symbol = best["symbol"]
            direction = best["direction"]

            print("STEP 4: position check")

            if has_position(symbol, direction):
                print("⛔ POSITION EXISTS")
                time.sleep(2)
                continue

            print("STEP 5: open position")
            open_position(best)

            print("STEP 6: send telegram")
            send_signal(best)

            print("📨 SENT TO TELEGRAM")

            time.sleep(2)

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(2)


if __name__ == "__main__":
    run()
