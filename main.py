import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(signal):

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

text = (
    "🚀 TRADE SIGNAL\n\n"
    f"Symbol: {signal['symbol']}\n"
    f"Direction: {signal['direction']}\n"
    f"Score: {signal['score']}\n"
    f"Entry: {signal['entry']}\n"
    f"SL: {signal['sl']}\n"
    f"TP: {signal['tp']}"
)

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": text
    }
)

print(response.text)

signal = {
"symbol": "BTCUSDT",
"direction": "BUY",
"score": 80,
"entry": 65000,
"sl": 64000,
"tp": 67000
}

send_signal(signal)
