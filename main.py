import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(signal):
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

```
text = (
    "🚀 TRADE SIGNAL\n\n"
    f"Symbol: {signal['symbol']}\n"
    f"Direction: {signal['direction']}\n"
    f"Score: {signal['score']}\n"
)

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": text
    }
)
```

signal = {
"symbol": "BTCUSDT",
"direction": "BUY",
"score": 80
}

send_signal(signal)
