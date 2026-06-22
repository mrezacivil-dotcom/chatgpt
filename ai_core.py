from collections import defaultdict

memory = defaultdict(lambda: {"win": 0, "loss": 0})


def update_memory(symbol, result):
    m = memory[symbol]

    if result == "WIN":
        m["win"] += 1
    else:
        m["loss"] += 1


def winrate(symbol):
    m = memory[symbol]
    total = m["win"] + m["loss"]

    if total == 0:
        return 0.5

    return m["win"] / total


def adaptive_score(symbol, base):
    wr = winrate(symbol)

    if wr > 0.65:
        return base * 1.2
    elif wr < 0.4:
        return base * 0.8

    return base
