import os
import time
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://api.bybit.com/v5/market/instruments-info"


def send_signal(signal):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        text = (
            "🚀 TRADE SIGNAL\n\n"
            f"Symbol: {signal['symbol']}\n"
            f"Direction: {signal['direction']}\n"
            f"Score: {signal['score']}\n"
        )

        r = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)

        print("Telegram:", r.text)

    except Exception as e:
        print("Telegram error:", e)


def get_symbols():
    try:
        r = requests.get(URL, params={"category": "linear"}, timeout=10)
        data = r.json()

        print("BYBIT RAW:", data)   # 🔥 مهم‌ترین دیباگ

        if "result" not in data:
            return []

        return [x["symbol"] for x in data["result"]["list"][:50]]

    except Exception as e:
        print("BYBIT ERROR:", e)
        return []


def analyze(symbol):
    return {
        "symbol": symbol,
        "direction": "BUY",
        "score": 80
    }


def run():
    print("BOT STARTED")

    symbols = get_symbols()

    print("SYMBOL COUNT:", len(symbols))

    if not symbols:
        print("❌ هیچ سمبلی نیومد -> مشکل API")
        return

    for s in symbols[:10]:
        signal = analyze(s)
        send_signal(signal)
        time.sleep(1)

    print("DONE")


if __name__ == "__main__":
    run()
