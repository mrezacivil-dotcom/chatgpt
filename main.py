import os
import requests

# خواندن Secrets از GitHub
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


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

        response = requests.post(url, data=payload)

        print("TOKEN EXISTS:", bool(BOT_TOKEN))
        print("CHAT EXISTS:", bool(CHAT_ID))
        print("Telegram response:", response.text)

    except Exception as e:
        print("Telegram error:", str(e))


# تست ارسال پیام
signal = {
    "symbol": "BTCUSDT",
    "direction": "BUY",
    "score": 85,
    "confidence": "HIGH",
    "entry": 65000,
    "sl": 64000,
    "tp": 67000,
    "regime": "TREND"
}

send_signal(signal)
send_signal(signal)

print("FINISHED")
exit()
