import os
import requests
import time

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(signal):
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

text = (
    "🚀 TRADE SIGNAL\n\n"
    f"Symbol: {signal['symbol']}\n"
    f"Direction: {signal['direction']}\n"
    f"Score: {signal['score']}\n\n"
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

def run():

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]

for symbol in symbols:

    signal = {
        "symbol": symbol,
        "direction": "BUY",
        "score": 80,
        "entry": 100,
        "sl": 95,
        "tp": 110
    }

    send_signal(signal)
    time.sleep(1)

if name == "main":
run()
