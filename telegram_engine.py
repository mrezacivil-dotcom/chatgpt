import requests
from config import BOT_TOKEN, CHAT_ID

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def format_price(price):
    """فرمت داینامیک قیمت برای ارزهای اعشاری زیاد مثل DOGE"""
    if price >= 1000: return f"{price:.2f}"
    if price >= 1: return f"{price:.4f}"
    if price >= 0.01: return f"{price:.6f}"
    return f"{price:.8f}"

def send_signal(signal):
    text = f"""
🚀 V65 SMART SIGNAL

🪙 {signal['symbol']} | {signal['direction']}

🎯 Entry: {format_price(signal['entry'])}
🛑 SL: {format_price(signal['sl'])}
✅ TP: {format_price(signal['tp'])}

📊 Score: {signal['score']}
🧠 Conf: {signal['confidence']}%
"""
    try:
        requests.post(URL, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
        print("📨 TG SENT OK")
    except Exception as e:
        print("TG ERROR:", e)
