import os
import time
import requests

# =========================
# LOAD ENV VARIABLES
# =========================
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


print("🚀 BOT STARTING...")
print("TOKEN LOADED:", bool(BOT_TOKEN))
print("CHAT_ID LOADED:", bool(CHAT_ID))


# =========================
# TELEGRAM SEND FUNCTION
# =========================
def send_telegram(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Missing TELEGRAM_TOKEN or CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        data = response.json()

        if data.get("ok"):
            print("✅ Message sent to Telegram")
        else:
            print("❌ Telegram API error:", data)

    except Exception as e:
        print("❌ Request error:", str(e))


# =========================
# MOCK SIGNAL (TEST)
# =========================
def get_signal():
    return {
        "symbol": "BTCUSDT",
        "direction": "BUY",
        "score": 85,
        "confidence": 0.78,
        "entry": 65000,
        "sl": 64000,
        "tp": 67000,
        "regime": "trend"
    }


# =========================
# MAIN LOOP
# =========================
def main():
    print("🚀 GITHUB SIGNAL BOT STARTED")

    signal = get_signal()
    print("SIGNAL:", signal)

    message = f"""
🚀 TRADE SIGNAL

Symbol: {signal['symbol']}
Direction: {signal['direction']}
Score: {signal['score']}
Confidence: {signal['confidence']}

Entry: {signal['entry']}
SL: {signal['sl']}
TP: {signal['tp']}
Regime: {signal['regime']}
"""

    send_telegram(message)


if __name__ == "__main__":
    main()
