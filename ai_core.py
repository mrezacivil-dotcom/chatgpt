import json
import os
from collections import defaultdict

MEMORY_FILE = "memory.json"

memory = defaultdict(lambda: {
    "win": 0,
    "loss": 0
})


def load_memory():
    global memory

    if not os.path.exists(MEMORY_FILE):
        return

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        for k, v in data.items():
            memory[k] = v

    except Exception as e:
        print("MEMORY LOAD ERROR:", e)


def save_memory():
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(dict(memory), f, indent=2)

    except Exception as e:
        print("MEMORY SAVE ERROR:", e)


load_memory()


def update_memory(symbol, result):

    if result == "WIN":
        memory[symbol]["win"] += 1
    else:
        memory[symbol]["loss"] += 1

    save_memory()


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
