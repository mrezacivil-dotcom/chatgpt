from dataclasses import dataclass

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


# =========================
# OPEN POSITION
# =========================
def open_position(signal):

    p = Position(
        symbol=signal["symbol"],
        direction=signal["direction"],
        entry=float(signal["entry"]),
        sl=float(signal["sl"]),
        tp=float(signal["tp"]),
        size=float(signal.get("size", 1.0))
    )

    positions.append(p)

    print(f"📌 OPENED: {p.symbol} {p.direction} | size={p.size}")

    return p


# =========================
# GET POSITIONS
# =========================
def get_positions():
    return positions


# =========================
# REAL POSITION CHECK (FIXED)
# =========================
def has_position(symbol, direction):

    for p in positions:
        if (
            p.symbol == symbol and
            p.direction == direction and
            p.status == "OPEN"
        ):
            return True

    return False


# =========================
# UPDATE POSITIONS
# =========================
def update_positions(price_feed):

    global positions

    new_positions = []

    for p in positions:

        price = price_feed(p.symbol)

        if not price:
            new_positions.append(p)
            continue

        if p.direction == "BUY":

            if price >= p.tp:
                p.status = "TP"
                continue

            if price <= p.sl:
                p.status = "SL"
                continue

        else:

            if price <= p.tp:
                p.status = "TP"
                continue

            if price >= p.sl:
                p.status = "SL"
                continue

        new_positions.append(p)

    positions = new_positions
