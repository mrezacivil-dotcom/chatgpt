import os
import time
import requests

# ===================== CONFIG =====================
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BYBIT_URL = "https://api.bybit.com/v5/market/instruments-info"

# ===================== TELEGRAM =====================
def send_signal(signal):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        text = (
            "🚀 TRADE SIGNAL\n\n"
            f"Symbol: {signal.get('symbol', 'N/A')}\n"
            f"Direction: {signal.get('direction', 'N/A')}\n"
            f"Score: {signal.get('score', 'N/A')}\n"
            f"Confidence: {signal.get('confidence', 'N/A')}\n\n"
            f"Entry: {signal.get('entry', 'N/A')}\n"
            f"SL: {signal.get('sl', 'N/A')}\n"
            f"TP: {signal.get('tp', 'N/A')}\n\n"
            f"Regime: {signal.get('regime', 'N/A')}"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }

        r = requests.post(url, data=payload, timeout=10)

        print("Telegram response:", r.text)

    except Exception as e:
        print("Telegram error:", str(e))


# ===================== BYBIT SYMBOLS =====================
def get_symbols():
    try:
        r = requests.get(BYBIT_URL, params={"category": "linear"}, timeout=10)
        data = r.json()

        if "result" not in data:
            print("Bybit error:", data)
            return []

        symbols = [
            item["symbol"]
            for item in data["result"]["list"]
            if item.get("status") == "Trading"
        ]

        return symbols

    except Exception as e:
        print("Symbol error:", str(e))
        return []


# ===================== SIMPLE SIGNAL ENGINE =====================
def analyze(symbol):
    # این بخش فعلاً ساده است (بعداً حرفه‌ایش می‌کنیم)
    return {
        "symbol": symbol,
        "direction": "BUY",
        "score": 80,
        "confidence": "HIGH",
        "entry": 100,
        "sl": 95,
        "tp": 110,
        "regime": "TREND"
    }


# ===================== MAIN LOOP =====================
def run():
    print("BOT STARTED...")

    if not BOT_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_TOKEN or CHAT_ID")
        return

    while True:
        symbols = get_symbols()

        print("Symbols loaded:", len(symbols))

        for s in symbols[:30]:  # سبک نگه داشتن
            signal = analyze(s)
            send_signal(signal)
            time.sleep(0.2)  # جلوگیری از اسپم تلگرام

        print("Cycle done. Sleeping...")
        time.sleep(60)


# ===================== START =====================
if __name__ == "__main__":
    run()
