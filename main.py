import os
import ccxt
import pandas as pd
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

exchange = ccxt.bybit({
    "enableRateLimit": True,
    "options": {"defaultType": "spot"}
})

timeframes = ["1h", "4h"]

# ================= INDICATORS =================
def ema(s, p):
    return s.ewm(span=p, adjust=False).mean()

def rsi(s, p=14):
    d = s.diff()
    g = d.where(d > 0, 0).rolling(p).mean()
    l = (-d.where(d < 0, 0)).rolling(p).mean()
    rs = g / l
    return 100 - (100 / (1 + rs))

def adx(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(p).mean()

    plus = h.diff().rolling(p).mean()
    minus = l.diff().rolling(p).mean()

    dx = (abs(plus - minus) / (plus + minus)) * 100
    return dx.rolling(p).mean()

# ================= TELEGRAM =================
def send(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    text = (
        "🚀 TRADE SIGNAL\n\n"
        f"{signal['symbol']} | {signal['timeframe']}\n"
        f"{signal['direction']} | Score: {signal['score']}\n"
        f"RSI: {signal['rsi']:.2f}\n\n"
        f"Entry: {signal['entry']}\nSL: {signal['sl']}\nTP: {signal['tp']}"
    )

    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# ================= SYMBOLS (SAFE MODE) =================
symbols = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "XRP/USDT",
    "DOGE/USDT",
    "BNB/USDT",
    "ADA/USDT",
    "AVAX/USDT"
]

# ================= SIGNAL =================
def check(df):
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"])
    df["adx"] = adx(df)

    last = df.iloc[-1]

    score = 0
    direction = None

    if last["ema50"] > last["ema200"]:
        direction = "BUY"
        score += 1
    else:
        direction = "SELL"
        score += 1

    if (direction == "BUY" and last["rsi"] < 70) or (direction == "SELL" and last["rsi"] > 30):
        score += 1

    if last["adx"] > 15:
        score += 1

    if score >= 3:
        price = last["close"]
        return {
            "symbol": df.attrs.get("symbol"),
            "timeframe": df.attrs.get("tf"),
            "direction": direction,
            "score": score,
            "rsi": float(last["rsi"]),
            "entry": price,
            "sl": price * (0.98 if direction == "BUY" else 1.02),
            "tp": price * (1.03 if direction == "BUY" else 0.97),
        }

# ================= MAIN =================
def run():
    for symbol in symbols:
        for tf in timeframes:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=200)

                df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])
                df.rename(columns={"c": "close", "h": "high", "l": "low"}, inplace=True)

                df.attrs["symbol"] = symbol
                df.attrs["tf"] = tf

                sig = check(df)
                if sig:
                    send(sig)

            except Exception as e:
                print("ERR:", symbol, tf, e)

if __name__ == "__main__":
    run()
    print("DONE")
