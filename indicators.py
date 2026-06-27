import numpy as np


def ema(values, period):
    """محاسبه EMA صحیح"""
    if len(values) < period:
        return None

    values = np.array(values, dtype=float)
    k = 2.0 / (period + 1)

    # شروع از SMA اولیه
    result = np.mean(values[:period])

    for i in range(period, len(values)):
        result = values[i] * k + result * (1 - k)

    return result


def sma(values, period):
    """میانگین ساده"""
    if len(values) < period:
        return None
    return np.mean(values[-period:])


def rsi(closes, period=14):
    """شاخص قدرت نسبی"""
    if len(closes) < period + 1:
        return 50.0

    closes = np.array(closes, dtype=float)
    deltas = np.diff(closes[-(period + 1):])

    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def atr(highs, lows, closes, period=14):
    """Average True Range واقعی"""
    if len(closes) < period + 1:
        return np.mean(np.abs(np.diff(closes[-period:])))

    highs = np.array(highs[-period - 1:], dtype=float)
    lows = np.array(lows[-period - 1:], dtype=float)
    closes = np.array(closes[-period - 1:], dtype=float)

    tr_list = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        tr_list.append(tr)

    return np.mean(tr_list)


def macd(closes, fast=12, slow=26, signal=9):
    """MACD اندیکاتور"""
    if len(closes) < slow + signal:
        return None, None, None

    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)

    if ema_fast is None or ema_slow is None:
        return None, None, None

    macd_line = ema_fast - ema_slow

    return macd_line, ema_fast, ema_slow


def bollinger_bands(closes, period=20, std_dev=2):
    """باندهای بولینگر"""
    if len(closes) < period:
        return None, None, None

    closes = np.array(closes[-period:], dtype=float)
    middle = np.mean(closes)
    std = np.std(closes)

    upper = middle + std_dev * std
    lower = middle - std_dev * std

    return upper, middle, lower


def volume_analysis(volumes, period=20):
    """آنالیز حجم"""
    if len(volumes) < period:
        return 1.0

    avg_vol = np.mean(volumes[-period:])
    current_vol = volumes[-1]

    if avg_vol == 0:
        return 1.0

    return current_vol / avg_vol


def support_resistance(highs, lows, closes, period=50):
    """سطوح حمایت و مقاومت"""
    if len(closes) < period:
        return closes[-1] * 0.98, closes[-1] * 1.02

    recent_lows = lows[-period:]
    recent_highs = highs[-period:]

    support = np.min(recent_lows)
    resistance = np.max(recent_highs)

    return support, resistance
