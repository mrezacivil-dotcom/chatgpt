import requests
from config import BOT_TOKEN, CHAT_ID


def get_url():
    """ساخت URL تلگرام"""
    if not BOT_TOKEN:
        print("⚠️ TELEGRAM TOKEN NOT SET")
        return None
    return f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_signal(signal):
    """ارسال سیگنال به تلگرام"""

    url = get_url()
    if not url or not CHAT_ID:
        print("⚠️ TELEGRAM NOT CONFIGURED")
        return False

    direction_emoji = "🟢" if signal["direction"] == "BUY" else "🔴"
    reasons = "\n".join(f"  • {r}" for r in signal.get("reasons", []))

    text = f"""
{direction_emoji} V65 PRO SIGNAL

📊 {signal['symbol']} — {signal['direction']}

💰 Entry: {signal['entry']:.4f}
🛑 SL: {signal['sl']:.4f}
🎯 TP: {signal['tp']:.4f}

📈 Score: {signal['score']}
🧠 Confidence: {signal['confidence']}%
📉 RSI: {signal.get('rsi', 'N/A')}

📝 Reasons:
{reasons}

⚙️ {signal.get('regime', 'V65')}
"""

    try:
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }, timeout=10)

        if response.status_code == 200:
            print("📨 TELEGRAM SENT ✅")
            return True
        else:
            print(f"⚠️ TELEGRAM ERROR: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ TELEGRAM ERROR: {e}")
        return False


def send_alert(message):
    """ارسال هشدار به تلگرام"""

    url = get_url()
    if not url or not CHAT_ID:
        return False

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": f"⚠️ ALERT: {message}"
        }, timeout=10)
        return True
    except:
        return False
