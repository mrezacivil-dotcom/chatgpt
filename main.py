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

# =========================
# MAIN LOOP
# =========================
def run():

    print("🚀 GITHUB SIGNAL BOT STARTED")

    while True:

        try:
            # =========================
            # UPDATE POSITIONS
            # =========================
            update_positions(get_price)

            # =========================
            # GET SIGNALS
            # =========================
            signals = get_signals()

            print("SIGNALS RAW:", signals)

            if not signals:
                print("📡 NO SIGNAL")
                time.sleep(2)
                continue

            best = max(signals, key=lambda x: x["score"])

            print("🔥 SIGNAL:", best)

            symbol = best["symbol"]
            direction = best["direction"]

            # =========================
            # POSITION CHECK
            # =========================
            if has_position(symbol, direction):
                print("⛔ POSITION EXISTS")
                time.sleep(2)
                continue

            # =========================
            # EXECUTION
            # =========================
            open_position(best)

            send_signal(best)

            print("📊 SENT TO TELEGRAM")

            time.sleep(2)

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(2)


if name == "main":
    run()
if name == "main":
    run()
