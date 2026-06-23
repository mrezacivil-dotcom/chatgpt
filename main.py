import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN EXISTS:", bool(BOT_TOKEN))
print("CHAT EXISTS:", bool(CHAT_ID))


def send_signal(signal):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Missing ENV variables")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

  text = (
    "🚀 TRADE SIGNAL\n\n"
    f"Symbol: {signal.get('symbol', 'N/A')}\n"
    f"Direction: {signal.get('direction', 'N/A')}\n"
    f"Score: {signal.get('score', 'N/A')}\n\n"
    f"Entry: {signal.get('entry', 'N/A')}\n"
    f"SL: {signal.get('sl', 'N/A')}\n"
    f"TP: {signal.get('tp', 'N/A')}"
)

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    r = requests.post(url, data=payload)
    print("Telegram response:", r.text)


# تست ساده
send_signal({
    "symbol": "BTCUSDT",
    "direction": "BUY",
    "score": 85,
    "entry": 65000,
    "sl": 64000,
    "tp": 67000
})
