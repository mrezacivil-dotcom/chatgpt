def fundamental_filter(symbol, direction):

    h = sum(ord(c) for c in symbol) % 100

    if h > 95 and direction == "BUY":
        return False

    if h < 5 and direction == "SELL":
        return False

    return True
