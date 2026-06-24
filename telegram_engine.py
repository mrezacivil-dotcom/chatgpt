import requests

BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_signal(signal):

    text = f"""
🚀 V62 SIGNAL

{signal['symbol']} {signal['direction']}

Entry: {signal['entry']:.4f}
SL: {signal['sl']:.4f}
TP: {signal['tp']:.4f}

Score: {signal['score']}
Conf: {signal['confidence']}%
"""

    try:
        requests.post(URL, data={
            "chat_id": CHAT_ID,
            "text": text
        })
        print("📨 TG SENT OK")

    except Exception as e:
        print("TG ERROR:", e)
