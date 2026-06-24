from collections import defaultdict

memory = defaultdict(lambda: {
    "win": 0,
    "loss": 0
})


def update_memory(symbol, result):

    if result == "WIN":
        memory[symbol]["win"] += 1
    else:
        memory[symbol]["loss"] += 1


def winrate(symbol):

    total = (
        memory[symbol]["win"] +
        memory[symbol]["loss"]
    )

    if total == 0:
        return 0.5

    return memory[symbol]["win"] / total


def adaptive_score(symbol, base):

    wr = winrate(symbol)

    if wr > 0.65:
        return base * 1.2

    if wr < 0.40:
        return base * 0.8

    return base


def adaptive_confidence(symbol, confidence):

    wr = winrate(symbol)

    if wr > 0.65:
        confidence += 5

    elif wr < 0.40:
        confidence -= 5

    return max(50, min(95, confidence))
