from dataclasses import dataclass

from ai_core import update_memory
from risk_engine import update_account

positions = []


@dataclass
class Position:

    symbol: str
    direction: str
    entry: float
    sl: float
    tp: float
    size: float = 1.0
    status: str = "OPEN"


def open_position(signal):

    if has_position(signal["symbol"]):
        return None

    p = Position(
        symbol=signal["symbol"],
        direction=signal["direction"],
        entry=float(signal["entry"]),
        sl=float(signal["sl"]),
        tp=float(signal["tp"]),
        size=float(signal.get("size", 1))
    )

    positions.append(p)

    print(
        f"📌 OPENED: "
        f"{p.symbol} "
        f"{p.direction}"
    )

    return p


def get_positions():
    return positions


def has_position(symbol):

    for p in positions:
        if p.symbol == symbol and p.status == "OPEN":
            return True

    return False


def update_positions(price_feed):

    global positions

    active = []

    for p in positions:

        price = price_feed(p.symbol)

        if price is None:
            active.append(p)
            continue

        if p.direction == "BUY":

            if price >= p.tp:
                p.status = "TP"
                update_memory(p.symbol, "WIN")
                update_account("WIN")
                continue

            if price <= p.sl:
                p.status = "SL"
                update_memory(p.symbol, "LOSS")
                update_account("LOSS")
                continue

        else:

            if price <= p.tp:
                p.status = "TP"
                update_memory(p.symbol, "WIN")
                update_account("WIN")
                continue

            if price >= p.sl:
                p.status = "SL"
                update_memory(p.symbol, "LOSS")
                update_account("LOSS")
                continue

        active.append(p)

    positions = active
