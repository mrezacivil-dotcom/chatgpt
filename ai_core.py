import os
import json
from collections import defaultdict

MEMORY_FILE = "ai_memory.json"

# بارگذاری حافظه از فایل
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        loaded_mem = json.load(f)
    memory = defaultdict(lambda: {"win": 0, "loss": 0}, loaded_mem)
else:
    memory = defaultdict(lambda: {"win": 0, "loss": 0})

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def update_memory(symbol, result):
    if result == "WIN":
        memory[symbol]["win"] += 1
    else:
        memory[symbol]["loss"] += 1
    save_memory() # هر تغییر را ذخیره می‌کند

def winrate(symbol):
    total = memory[symbol]["win"] + memory[symbol]["loss"]
    if total == 0:
        return 0.5
    return memory[symbol]["win"] / total

def adaptive_score(symbol, base):
    wr = winrate(symbol)
    if wr > 0.65: return base * 1.2
    if wr < 0.40: return base * 0.8
    return base

def adaptive_confidence(symbol, confidence):
    wr = winrate(symbol)
    if wr > 0.65: confidence += 5
    elif wr < 0.40: confidence -= 5
    return max(50, min(95, confidence))
