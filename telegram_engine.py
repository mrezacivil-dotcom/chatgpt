import requests
import time
from config import BOT_TOKEN, CHAT_ID

_last = 0
COOLDOWN = 5


def send_telegram(signal):

    global _last

    if time.time() - _last < COOLDOWN:
        return False

    text = (
        f"🚀 {signal.get('regime','V52')} SIGNAL\n\n"
        f"{signal['symbol']} {signal['direction']}\n\n"
        f"Entry: {signal['entry']:.4f}\n"
        f"SL: {signal['sl']:.4f}\n"
        f"TP: {signal['tp']:.4f}\n\n"
        f"Score: {signal['score']:.2f}\n"
        f"Conf: {signal['confidence']:.1f}%"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        r = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)

        if r.ok:
            _last = time.time()

        print("📨 TG:", r.text)
        return r.ok

    except Exception as e:
        print("TG ERROR:", e)
        return False
