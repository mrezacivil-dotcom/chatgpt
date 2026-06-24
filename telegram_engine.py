import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_signal(signal):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = f"""
🚀 SIGNAL

{signal['symbol']} {signal['direction']}

Entry: {signal['entry']}
SL: {signal['sl']}
TP: {signal['tp']}

Score: {signal['score']}
Confidence: {signal['confidence']}
"""

    try:

        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=20
        )

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

    except Exception as e:
        print("TELEGRAM ERROR:", str(e))
