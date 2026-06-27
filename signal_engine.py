import time
import numpy as np
from price_engine import get_klines
from ai_core import adaptive_score
from funding_engine import get_funding_bias, funding_filter
from fundamental_engine import fundamental_filter
from config import ENABLE_FUNDING, MIN_SCORE

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "DOGEUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT", "SUIUSDT", "WLDUSDT"
]

CACHE_SECONDS = 5
COOLDOWN_SECONDS = 45

_last_scan = 0
last_signal_time = {}

def ema(values, period):
    if len(values) < period:
        return None
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    return np.convolve(values, weights, mode='valid')[-1]

def true_atr(highs, lows, closes, period=14):
    if len(highs) < period + 1:
        return None
    tr_list = []
    for i in range(-period, 0):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
            abs(lows[i] - closes[i-1])
        )
        tr_list.append(tr)
    return np.mean(tr_list)

def cooldown_ok(symbol):
    now = time.time()
    if symbol in last_signal_time:
        if now - last_signal_time[symbol] < COOLDOWN_SECONDS:
            return False
    return True

def get_signals():
    global _last_scan
    if time.time() - _last_scan < CACHE_SECONDS:
        return []
    _last_scan = time.time()

    signals = []

    for symbol in SYMBOLS:
        data = get_klines(symbol)
        closes = data["closes"]
        highs = data["highs"]
        lows = data["lows"]

        if len(closes) < 200:
            continue
        if not cooldown_ok(symbol):
            continue

        price = closes[-1]
        if price <= 0:
            continue

        # محاسبه EMA ها
        ema50 = ema(closes, 50)
        ema200 = ema(closes, 200)

        if ema50 is None or ema200 is None:
            continue

        direction = "BUY" if ema50 > ema200 else "SELL"

        # فیلتر فاندینگ ریت (اگر فعال باشد)
        if ENABLE_FUNDING:
            bias = get_funding_bias(symbol)
            if not funding_filter(direction, bias):
                continue

        # فیلتر فاندمنتال (Placeholder)
        if not fundamental_filter(symbol, direction):
            continue

        base_score = 2.2
        if abs(ema50 - ema200) / price > 0.002:
            base_score += 0.3

        score = adaptive_score(symbol, base_score)
        if score < MIN_SCORE:
            continue

        # محاسبه دقیق ATR برای حد ضرر و سود
        atr = true_atr(highs, lows, closes)
        if atr is None or atr == 0:
            continue

        if direction == "BUY":
            sl = price - atr * 1.5
            tp = price + atr * 3.0
        else:
            sl = price + atr * 1.5
            tp = price - atr * 3.0

        confidence = min(92, 55 + score * 12)

        signals.append({
            "symbol": symbol,
            "direction": direction,
            "entry": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "score": round(score, 2),
            "confidence": round(confidence, 1),
            "regime": "V65_SMART_BRAIN"
        })

        last_signal_time[symbol] = time.time()

    return signals
