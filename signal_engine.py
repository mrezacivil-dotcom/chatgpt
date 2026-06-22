import time
import numpy as np
from price_engine import get_klines
from ai_core import adaptive_score

SYMBOLS = [
    "BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","DOTUSDT","LINKUSDT"
]

# =========================
# MEMORY
# =========================
_last_time = 0
last_signal_time = {}
last_trend = {}

CACHE_SECONDS = 5
COOLDOWN_SECONDS = 30

# =========================
# INDICATORS
# =========================
def volatility(closes):
    closes = np.array(closes[-50:])
    return np.std(closes) / closes[-1]

def ema(values, period):
    values = np.array(values)
    if len(values) < period:
        return None

    k = 2 / (period + 1)
    e = values[0]

    for v in values:
        e = v * k + e * (1 - k)

    return e

# =========================
# TREND FILTER (SOFT)
# =========================
def trend_stable(symbol, direction):
    if symbol in last_trend:
        if last_trend[symbol] == direction:
            return True   # نرم شد
    last_trend[symbol] = direction
    return True

# =========================
# COOLDOWN
# =========================
def cooldown_ok(symbol):
    now = time.time()

    if symbol in last_signal_time:
        if now - last_signal_time[symbol] < COOLDOWN_SECONDS:
            return False

    last_signal_time[symbol] = now
    return True

# =========================
# MAIN ENGINE
# =========================
def get_signals():
    global _last_time

    if time.time() - _last_time < CACHE_SECONDS:
        return []

    _last_time = time.time()

    signals = []

    for s in SYMBOLS:

        closes = get_klines(s)

        if not closes or len(closes) < 200:
            continue

        price = closes[-1]

        # =========================
        # VOLATILITY FILTER (SOFT)
        # =========================
        vol = volatility(closes)
        if vol < 0.0001:
            continue

        ema50 = ema(closes[-50:], 50)
        ema200 = ema(closes[-200:], 200)

        if ema50 is None or ema200 is None:
            continue

        trend = "BUY" if ema50 > ema200 else "SELL"

        # =========================
        # COOLDOWN
        # =========================
        if not cooldown_ok(s):
            continue

        # =========================
        # BASE SCORE
        # =========================
        base = 2.0

        if abs(ema50 - ema200) / price > 0.002:
            base += 0.5

        # =========================
        # AI SCORE
        # =========================
        score = adaptive_score(s, base)

        # =========================
        # FINAL FILTER (RELAXED)
        # =========================
        if score < 1.7:
            continue

        # =========================
        # TP / SL
        # =========================
        atr = np.mean(np.abs(np.diff(closes[-14:])))

        if trend == "BUY":
            sl = price - atr * 1.5
            tp = price + atr * 3
        else:
            sl = price + atr * 1.5
            tp = price - atr * 3

        confidence = min(90, 50 + score * 15)

        signals.append({
    "symbol": s,
    "direction": "BUY",
    "entry": price,
    "sl": price * 0.99,
    "tp": price * 1.01,
    "score": 2.0,
    "confidence": 80,
    "regime": "TEST_MODE"
})
break

    return signals
    print("DEBUG:", s, len(closes), vol, score)
