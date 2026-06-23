import os
import ccxt
import pandas as pd
import requests

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

exchange = ccxt.bybit({
    "enableRateLimit": True,
    "options": {"defaultType": "spot"}
})

timeframes = ["1h", "4h"]

symbols = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT",
    "XRP/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT"
]

# ======================
# INDICATORS
# ======================
def ema(s, p):
    return s.ewm(span=p, adjust=False).mean()

def rsi(s, p=14):
    d = s.diff()
    g = d.where(d > 0, 0).rolling(p).mean()
    l = (-d.where(d < 0, 0)).rolling(p).mean()
    rs = g / l
    return 100 - (100 / (1 + rs))

def volatility(df):
    return (df["high"] - df["low"]).rolling(14).mean()

# ======================
# TELEGRAM
# ======================
def send(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = (
        "🚀 HIGH ACCURACY SIGNAL\n\n"
        f"{signal['symbol']} | {signal['timeframe']}\n"
        f"{signal['direction']} | Score: {signal['score']}\n"
        f"RSI: {signal['rsi']:.2f}\nVol: {signal['vol']:.2f}\n\n"
        f"Entry: {signal['entry']}\n"
        f"SL: {signal['sl']}\n"
        f"TP: {signal['tp']}"
    )

    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# ======================
# SIGNAL ENGINE (SMART)
# ======================
def check(df):
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"])
    df["vol"] = volatility(df)

    last = df.iloc[-1]

    score = 0
    direction = None

    # Trend filter (MAIN)
    if last["ema50"] > last["ema200"]:
        direction = "BUY"
        score += 2
    elif last["ema50"] < last["ema200"]:
        direction = "SELL"
        score += 2
    else:
        return None

    # RSI confirmation (strict)
    if direction == "BUY" and 45 < last["rsi"] < 70:
        score += 1
    elif direction == "SELL" and 30 < last["rsi"] < 55:
        score += 1
    else:
        score -= 1  # weak condition

    # Volatility filter (avoid flat market)
    if last["vol"] > df["vol"].mean():
        score += 1

    # FINAL QUALITY FILTER (important)
    if score < 3:
        return None

    price = last["close"]

    return {
        "direction": direction,
        "score": score,
        "rsi": float(last["rsi"]),
        "vol": float(last["vol"]),
        "entry": price,
        "sl": price * (0.985 if direction == "BUY" else 1.015),
        "tp": price * (1.025 if direction == "BUY" else 0.975),
    }

# ======================
# MAIN LOOP
# ======================
def run():
    print("Scanning market...")

    for symbol in symbols:
        for tf in timeframes:
            try:
                df = exchange.fetch_ohlcv(symbol, tf, limit=200)
                df = pd.DataFrame(df, columns=["t","o","h","l","c","v"])
                df.rename(columns={"c":"close","h":"high","l":"low"}, inplace=True)

                signal = check(df)

                if signal:
                    signal["symbol"] = symbol
                    signal["timeframe"] = tf
                    send(signal)
                    print("SENT:", symbol, tf, signal["direction"])

            except Exception as e:
                print("ERROR:", symbol, tf, e)

if __name__ == "__main__":
    run()
    print("DONE")
