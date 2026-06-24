import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_signal(signal):
    text = f"""
🚀 SIGNAL

{signal['symbol']} {signal['direction']}

Entry: {signal['entry']}
SL: {signal['sl']}
TP: {signal['tp']}

Score: {signal['score']}
Confidence: {signal['confidence']}
"""

    requests.post(URL, data={
        "chat_id": CHAT_ID,
        "text": text
    })
