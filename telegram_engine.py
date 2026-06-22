import os
import requests

# اگر از GitHub Secrets استفاده کردی:
# 0

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_signal(signal):

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        text = f"""
🚀 TRADE SIGNAL

Symbol: {signal.get('symbol', 'N/A')}
Direction: {signal.get('direction', 'N/A')}
Score: {signal.get('score', 'N/A')}
Confidence: {signal.get('confidence', 'N/A')}

Entry: {signal.get('entry', 'N/A')}
SL: {signal.get('sl', 'N/A')}
TP: {signal.get('tp', 'N/A')}

Regime: {signal.get('regime', 'N/A')}
"""

        payload = {
            "chat_id": CHAT_ID,
            "text": text
        }

        response = requests.post(url, data=payload)

        print("📨 Telegram response:", response.text)

    except Exception as e:
        print("❌ Telegram error:", str(e))
