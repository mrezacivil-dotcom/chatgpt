import time
import numpy as np

from price_engine import get_klines
from ai_core import adaptive_score


SYMBOLS = [
    "BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","DOTUSDT","LINKUSDT"
]

_last_time = 0

# =========================
# SIGNAL MEMORY (V63 CORE)
# =========================
last_signal_time = {}
last_trend = {}


CACHE_SECONDS = 5
COOLDOWN_SECONDS = 45   # مهم: V63 stronger than V62


# =========================
# INDICATORS
# =========================
def volatility(closes):
    return np.std(closes[-50:]) / closes[-1]


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
# TREND STABILITY FILTER (NEW V63)
# =========================
def trend_stable(symbol, direction):

    if symbol in last_trend:
        if last_trend[symbol] == direction:
            return False  # جلوگیری از spam same trend

    last_trend[symbol] = direction
    return True


# =========================
# COOLDOWN PER SYMBOL
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

        if len(closes) < 100:
            continue

        price = closes[-1]

        # =========================
        # V63 FILTER: NOISE REMOVAL
        # =========================
        vol = volatility(closes)
        if vol < 0.00025:
            continue

        ema50 = ema(closes[-50:], 50)
        ema200 = ema(closes[-200:], 200)

        if ema50 is None or ema200 is None:
            continue

        trend = "BUY" if ema50 > ema200 else "SELL"

        # =========================
        # V63 CORE INTELLIGENCE
        # =========================

        # 1. trend stability filter
        if not trend_stable(s, trend):
            continue

        # 2. cooldown filter
        if not cooldown_ok(s):
            continue

        # =========================
        # BASE STRUCTURE SCORE
        # =========================
        base = 2.2

        if abs(ema50 - ema200) / price > 0.002:
            base *= 1.2

        # =========================
        # AI ADAPTIVE SCORE
        # =========================
        score = adaptive_score(s, base)

        # =========================
        # FINAL FILTER (V63 stricter)
        # =========================
        if score < 2.3:
            continue

        # =========================
        # TP / SL (ATR STYLE SIMPLE)
        # =========================
        atr = np.mean(np.abs(np.diff(closes[-14:])))

        sl = price - atr * 1.5 if trend == "BUY" else price + atr * 1.5
        tp = price + atr * 3 if trend == "BUY" else price - atr * 3

        confidence = min(92, 55 + score * 12)

        signals.append({
            "symbol": s,
            "direction": trend,
            "entry": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "score": round(score, 2),
            "confidence": round(confidence, 1),
            "regime": "V63_SMART_BRAIN"
        })

    return signals
