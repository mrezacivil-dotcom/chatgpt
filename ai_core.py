from collections import defaultdict
import time
import json
import os

# حافظه هوشمند
memory = defaultdict(lambda: {
    "wins": 0,
    "losses": 0,
    "total_profit": 0.0,
    "last_signals": [],
    "best_hour": None,
    "avg_duration": 0
})

MEMORY_FILE = "ai_memory.json"


def save_memory():
    """ذخیره حافظه در فایل"""
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(dict(memory), f, indent=2)
    except Exception as e:
        print(f"⚠️ SAVE MEMORY ERROR: {e}")


def load_memory():
    """بارگذاری حافظه از فایل"""
    global memory
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    memory[k] = v
            print(f"✅ MEMORY LOADED: {len(data)} symbols")
    except Exception as e:
        print(f"⚠️ LOAD MEMORY ERROR: {e}")


def update_memory(symbol, result, profit=0.0):
    """بروزرسانی حافظه با نتیجه ترید"""
    if result == "WIN":
        memory[symbol]["wins"] += 1
    else:
        memory[symbol]["losses"] += 1

    memory[symbol]["total_profit"] += profit

    # ذخیره آخرین سیگنال‌ها
    memory[symbol]["last_signals"].append({
        "result": result,
        "profit": profit,
        "time": time.time()
    })

    # فقط ۵۰ سیگنال آخر را نگه دار
    if len(memory[symbol]["last_signals"]) > 50:
        memory[symbol]["last_signals"] = memory[symbol]["last_signals"][-50:]

    save_memory()


def winrate(symbol):
    """محاسبه وین‌ریت"""
    total = memory[symbol]["wins"] + memory[symbol]["losses"]
    if total == 0:
        return 0.5
    return memory[symbol]["wins"] / total


def total_trades(symbol):
    """تعداد کل ترید"""
    return memory[symbol]["wins"] + memory[symbol]["losses"]


def adaptive_score(symbol, base_score):
    """امتیاز تطبیقی بر اساس عملکرد"""
    wr = winrate(symbol)
    trades = total_trades(symbol)

    # اگر ترید کافی نداشته، تغییر نده
    if trades < 5:
        return base_score

    if wr > 0.70:
        return base_score * 1.3
    elif wr > 0.60:
        return base_score * 1.15
    elif wr < 0.35:
        return base_score * 0.6
    elif wr < 0.45:
        return base_score * 0.8

    return base_score


def adaptive_confidence(symbol, confidence):
    """اعتماد تطبیقی"""
    wr = winrate(symbol)
    trades = total_trades(symbol)

    if trades < 5:
        return confidence

    if wr > 0.65:
        confidence += 8
    elif wr > 0.55:
        confidence += 3
    elif wr < 0.40:
        confidence -= 10
    elif wr < 0.45:
        confidence -= 5

    return max(40, min(95, confidence))


def get_symbol_stats(symbol):
    """آمار کامل یک سیمبل"""
    return {
        "winrate": round(winrate(symbol) * 100, 1),
        "total": total_trades(symbol),
        "wins": memory[symbol]["wins"],
        "losses": memory[symbol]["losses"],
        "profit": round(memory[symbol]["total_profit"], 4)
    }


# بارگذاری حافظه هنگام شروع
load_memory()
