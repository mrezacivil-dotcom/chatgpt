import os
import time
import requests
import ccxt
import pandas as pd

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BYBIT = ccxt.bybit({
    "enableRateLimit": True,
    "timeout": 10000
})

TIMEFRAMES = ["1h", "4h"]

# ================== TELEGRAM ==================
def send_signal(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = (
        "🚀 TRADE SIGNAL\n\n"
        f"Symbol: {signal['symbol']}\n"
        f"TF: {signal['tf']}\n"
        f"Direction: {signal['side']}\n"
        f"Score: {signal['score']}\n\n"
        f"Entry: {signal['entry']}\n"
        f"SL: {signal['sl']}\n"
        f"TP: {signal['tp']}"
    )

    try:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": text},
            timeout=10
        )
        print("📨 SENT:", signal["symbol"])
    except Exception as e:
        print("Telegram error:", e)


# ================== INDICATOR ==================
def get_signal(df):
    df["ema_fast"] = df["close"].ewm(span=20).mean()
    df["ema_slow"] = df["close"].ewm(span=50).mean()

    if df["ema_fast"].iloc[-1] > df["ema_slow"].iloc[-1]:
        return "BUY", 80
    elif df["ema_fast"].iloc[-1] < df["ema_slow"].iloc[-1]:
        return "SELL", 80

    return None, 0


# ================== FETCH DATA ==================
def fetch(symbol, tf):
    try:
        ohlcv = BYBIT.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","vol"])
        return df
    except Exception as e:
        print("Fetch error:", symbol, tf, e)
        return None


# ================== MAIN LOOP ==================
def run():
    markets = BYBIT.load_markets()
    symbols = [s for s in markets if "/USDT" in s]

    print("STARTED - symbols:", len(symbols))

    while True:
        for symbol in symbols:

            for tf in TIMEFRAMES:
                df = fetch(symbol, tf)
                if df is None or len(df) < 50:
                    continue

                side, score = get_signal(df)

                if score >= 80:
                    signal = {
                        "symbol": symbol,
                        "tf": tf,
                        "side": side,
                        "score": score,
                        "entry": df["close"].iloc[-1],
                        "sl": df["close"].iloc[-1] * 0.98,
                        "tp": df["close"].iloc[-1] * 1.03
                    }

                    send_signal(signal)

        print("CYCLE DONE")
        time.sleep(60)


if __name__ == "__main__":
    run()
