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
    "options": {
        "defaultType": "spot"
    }
})

timeframes = ["1h", "4h"]


# ======================
# INDICATORS
# ======================
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def adx(df, period=14):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_dm = high.diff()
    minus_dm = low.diff()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return dx.rolling(period).mean()


# ======================
# TELEGRAM
# ======================
def send_signal(signal):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        text = (
            "🚀 TRADE SIGNAL\n\n"
            f"Symbol: {signal['symbol']}\n"
            f"Timeframe: {signal['timeframe']}\n"
            f"Direction: {signal['direction']}\n"
            f"Score: {signal['score']}\n"
            f"RSI: {signal['rsi']:.2f}\n\n"
            f"Entry: {signal['entry']}\n"
            f"SL: {signal['sl']}\n"
            f"TP: {signal['tp']}"
        )

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        })

        print("SENT:", signal["symbol"], signal["direction"])

    except Exception as e:
        print("Telegram error:", e)


# ======================
# SIGNAL ENGINE
# ======================
def check_signal(df):
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"])
    df["adx"] = adx(df)

    last = df.iloc[-1]

    score = 0
    direction = None

    # Trend
    if last["ema50"] > last["ema200"]:
        direction = "BUY"
        score += 1
    elif last["ema50"] < last["ema200"]:
        direction = "SELL"
        score += 1

    # RSI filter
    if direction == "BUY" and last["rsi"] < 70:
        score += 1
    if direction == "SELL" and last["rsi"] > 30:
        score += 1

    # ADX filter
    if last["adx"] > 18:
        score += 1

    if score >= 3:
        return {
            "direction": direction,
            "score": score,
            "rsi": float(last["rsi"]),
            "entry": float(last["close"]),
            "sl": float(last["close"] * (0.98 if direction == "BUY" else 1.02)),
            "tp": float(last["close"] * (1.03 if direction == "BUY" else 0.97)),
        }

    return None


# ======================
# MAIN LOOP
# ======================
def run():
    markets = exchange.load_markets()

    symbols = [
        s for s in markets
        if "/USDT" in s and markets[s]["active"]
    ]

    print(f"Scanning {len(symbols)} symbols...")

    for symbol in symbols:
        for tf in timeframes:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=200)

                df = pd.DataFrame(
                    ohlcv,
                    columns=["time", "open", "high", "low", "close", "volume"]
                )

                signal = check_signal(df)

                if signal:
                    signal["symbol"] = symbol
                    signal["timeframe"] = tf
                    send_signal(signal)

            except Exception as e:
                print("Error:", symbol, tf, str(e))


if __name__ == "__main__":
    run()
    print("FINISHED")
