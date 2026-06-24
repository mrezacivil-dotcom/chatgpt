import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_signal(signal):

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Missing Telegram credentials")
        print("BOT_TOKEN:", 8819076931:AAFTJn6zwoGHfnRe_LEnuoYwkS8GbGj2Fe4)
        print("CHAT_ID:", 5039122077)
        return

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

    try:
        response = requests.post(url, data=payload)
        data = response.json()

        if data.get("ok"):
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Telegram API error:", data)

    except Exception as e:
        print("❌ Request failed:", str(e))
