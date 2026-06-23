import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = "https://api.bybit.com"


# ================= TELEGRAM =================
def send_signal(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = (
        "🚀 TRADE SIGNAL\n\n"
        f"{signal['symbol']}\n"
        f"{signal['direction']} | Score: {signal['score']}\n"
        f"Entry: {signal['entry']} | SL: {signal['sl']} | TP: {signal['tp']}"
    )

    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Telegram:", r.text)


# ================= SYMBOLS (FIXED) =================
def get_symbols():
    try:
        url = f"{BASE_URL}/v5/market/instruments-info"
        r = requests.get(url, params={"category": "spot"}, timeout=10)

        data = r.json()
        print("BYBIT STATUS:", data.get("retMsg", "NO MSG"))

        if "result" not in data:
            return []

        return [x["symbol"] for x in data["result"]["list"][:20]]

    except Exception as e:
        print("BYBIT ERROR:", e)
        return []


# ================= SIMPLE STRATEGY =================
def analyze(symbol):
    return {
        "symbol": symbol,
        "direction": "BUY",
        "score": 75,
        "entry": 100,
        "sl": 95,
        "tp": 110
    }


# ================= MAIN LOOP =================
def run():
    print("BOT STARTED")

    symbols = get_symbols()

    print("SYMBOLS:", len(symbols))

    if len(symbols) == 0:
        print("❌ NO SYMBOLS -> BYBIT BLOCK / API ISSUE")
        return

    sent = 0

    for s in symbols:
        signal = analyze(s)
        send_signal(signal)
        sent += 1
        time.sleep(1)

    print("DONE SENT:", sent)


if __name__ == "__main__":
    run()
