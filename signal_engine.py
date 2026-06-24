import time
import numpy as np

from price_engine import get_klines
from ai_core import adaptive_score


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "DOTUSDT",
    "LINKUSDT",
    "SUIUSDT",
    "WLDUSDT"
]


CACHE_SECONDS = 5
COOLDOWN_SECONDS = 45

_last_scan = 0
last_signal_time = {}


# =========================
# EMA
# =========================
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
# VOLATILITY
# =========================
def volatility(closes):

    return np.std(closes[-50:]) / closes[-1]


# =========================
# COOLDOWN
# =========================
def cooldown_ok(symbol):

    now = time.time()

    if symbol in last_signal_time:
        if now - last_signal_time[symbol] < COOLDOWN_SECONDS:
            return False

    return True


# =========================
# MAIN
# =========================
def get_signals():

    global _last_scan

    if time.time() - _last_scan < CACHE_SECONDS:
        return []

    _last_scan = time.time()

    signals = []

    for symbol in SYMBOLS:

        closes = get_klines(symbol)

        if len(closes) < 200:
            continue

        if not cooldown_ok(symbol):
            continue

        price = closes[-1]

        vol = volatility(closes)

        if vol < 0.0002:
            continue
if vol < MIN_VOL:
    continue
if vol < MIN_VOL:
    continue

trend_strength = abs(ema50 - ema200) / price

if trend_strength < MIN_TREND:
    continue
   if score < MIN_SCORE:
    continue
   confidence = min(
    95,
    round(
        50 +
        trend_strength * 5000 +
        vol * 1000,
        1
    )
)    
trend_strength = abs(ema50 - ema200) / price

if trend_strength < MIN_TREND:
    continue
        ema50 = ema(closes[-50:], 50)
        ema200 = ema(closes[-200:], 200)

        if ema50 is None or ema200 is None:
            continue

        # LONG / SHORT
        direction = "BUY" if ema50 > ema200 else "SELL"

        base_score = 2.2

        if abs(ema50 - ema200) / price > 0.002:
            base_score += 0.3

        score = adaptive_score(symbol, base_score)

        if score < 2.0:
            continue

        atr = np.mean(np.abs(np.diff(closes[-14:])))

        if direction == "BUY":
            sl = price - atr * 1.5
            tp = price + atr * 3
        else:
            sl = price + atr * 1.5
            tp = price - atr * 3

        confidence = min(92, 55 + score * 12)

        signals.append({
            "symbol": symbol,
            "direction": direction,
            "entry": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "score": round(score, 2),
            "confidence": round(confidence, 1),
            "regime": "V64_SMART_BRAIN"
        })

        last_signal_time[symbol] = time.time()

    return signals
