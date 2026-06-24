import time
import numpy as np
from price_engine import get_ohlcv
from ai_core import adaptive_score
from config import MIN_SCORE, CACHE_SECONDS

SYMBOLS = [
    "BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","DOTUSDT","LINKUSDT",
    "SUIUSDT","WLDUSDT","TRXUSDT","LTCUSDT","ATOMUSDT",
    "NEARUSDT","ARBUSDT","OPUSDT","APTUSDT","FILUSDT",
    "INJUSDT","ICPUSDT","ETCUSDT","AAVEUSDT","RUNEUSDT",
    "GALAUSDT","SEIUSDT","TIAUSDT","HBARUSDT","MATICUSDT"
]

_last_scan = 0


def ema(values, period):
    if len(values) < period:
        return None

    values = np.array(values)
    k = 2 / (period + 1)

    e = values[0]
    for v in values:
        e = v * k + e * (1 - k)

    return e


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50

    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(high, low, close, period=14):
    if len(close) < period + 2:
        return 0

    trs = []
    for i in range(1, len(close)):
        tr = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1])
        )
        trs.append(tr)

    return np.mean(trs[-period:])


def volume_spike(volume):
    if len(volume) < 20:
        return 1

    avg = np.mean(volume[-20:])
    return volume[-1] / avg if avg > 0 else 1


def get_signals():
    global _last_scan

    if time.time() - _last_scan < CACHE_SECONDS:
        return []

    _last_scan = time.time()

    signals = []

    for symbol in SYMBOLS:

        data = get_ohlcv(symbol)

        closes = data["close"]
        highs = data["high"]
        lows = data["low"]
        volume = data["volume"]

        if len(closes) < 200:
            continue

        price = closes[-1]

        ema50 = ema(closes[-50:], 50)
        ema200 = ema(closes[-200:], 200)

        if ema50 is None or ema200 is None:
            continue

        trend_up = ema50 > ema200

        r = rsi(closes)
        a = atr(highs, lows, closes)
        v = volume_spike(volume)

        if v < 0.8:
            continue

        if trend_up and 55 < r < 75:
            direction = "BUY"
        elif not trend_up and 25 < r < 45:
            direction = "SELL"
        else:
            continue

        base_score = 2.5

        if abs(ema50 - ema200) / price > 0.003:
            base_score += 0.3

        if v > 1.5:
            base_score += 0.2

        score = adaptive_score(symbol, base_score)

        if score < MIN_SCORE:
            continue

        if direction == "BUY":
            sl = price - a * 1.5
            tp = price + a * 3
        else:
            sl = price + a * 1.5
            tp = price - a * 3

        confidence = min(92, 60 + score * 10)

        signals.append({
            "symbol": symbol,
            "direction": direction,
            "entry": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "score": round(score, 2),
            "confidence": round(confidence, 1),
            "regime": "V64_STABLE"
        })

    return signals
