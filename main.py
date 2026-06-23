import os
import time
import requests
import ccxt
import pandas as pd

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

exchange = ccxt.bybit({
    "enableRateLimit": True,
    "timeout": 10000,
    "options": {
        "defaultType": "swap"
    }
})

TIMEFRAMES = ["1h", "4h"]

# ================= TELEGRAM =================
def send_signal(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = (
        "🚀 TRADE SIGNAL\n\n"
        f"Symbol: {signal['symbol']}\n"
        f"TF: {signal['tf']}\n"
        f"Side: {signal['side']}\n"
        f"Score: {signal['score']}\n\n"
        f"Entry: {signal['entry']}\n"
        f"SL: {signal['sl']}\n"
        f"TP: {signal['tp']}"
    )

    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print("SENT:", signal["symbol"])
    except Exception as e:
        print("Telegram error:", e)


# ================= INDICATOR =================
def signal(df):
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()

    if df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:
        return "BUY", 80
    elif df["ema20"].iloc[-1] < df["ema50"].iloc[-1]:
        return "SELL", 80

    return None, 0


# ================= FETCH =================
def get_data(symbol, tf):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])
        return df
    except Exception as e:
        print("fetch error:", symbol, e)
        return None


# ================= SYMBOLS (SAFE) =================
def get_symbols():
    markets = exchange.load_markets()
    symbols = []

    for s in markets:
        if s.endswith("/USDT") and markets[s]["active"]:
            symbols.append(s)

    return symbols[:30]   # 👈 مهم: محدود شده برای جلوگیری از هنگ


# ================= MAIN =================
def run():
    symbols = get_symbols()
    print("Symbols loaded:", len(symbols))

    while True:
        for symbol in symbols:
            for tf in TIMEFRAMES:

                df = get_data(symbol, tf)
                if df is None or len(df) < 50:
                    continue

                side, score = signal(df)

                if score >= 80:
                    last = df["c"].iloc[-1]

                    send_signal({
                        "symbol": symbol,
                        "tf": tf,
                        "side": side,
                        "score": score,
                        "entry": last,
                        "sl": last * 0.98,
                        "tp": last * 1.03
                    })

        print("cycle done")
        time.sleep(60)


if __name__ == "__main__":
    run()
