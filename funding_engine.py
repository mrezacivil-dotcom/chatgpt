def get_funding_bias(symbol):
    h = sum(ord(c) for c in symbol) % 100

    if h > 70:
        return "OVERLONG"
    elif h < 30:
        return "OVERSHORT"

    return "NEUTRAL"


def funding_filter(direction, bias):

    if bias == "OVERLONG" and direction == "BUY":
        return False

    if bias == "OVERSHORT" and direction == "SELL":
        return False

    return True
