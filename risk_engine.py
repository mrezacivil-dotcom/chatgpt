from config import (
    MAX_DRAWDOWN, MAX_LOSS_STREAK,
    DEFAULT_BALANCE, MAX_RISK_PER_TRADE,
    MIN_RISK_PER_TRADE
)

account = {
    "balance": DEFAULT_BALANCE,
    "equity": DEFAULT_BALANCE,
    "loss_streak": 0,
    "win_streak": 0,
    "total_trades": 0,
    "total_wins": 0,
    "total_losses": 0,
    "peak_balance": DEFAULT_BALANCE,
    "max_drawdown_seen": 0
}


def trading_allowed():
    """آیا ترید مجاز است؟"""

    if account["balance"] <= 0:
        print("⛔ BALANCE ZERO")
        return False

    # محاسبه دراداون از بالاترین نقطه
    drawdown = (
        account["peak_balance"] - account["equity"]
    ) / account["peak_balance"]

    account["max_drawdown_seen"] = max(
        account["max_drawdown_seen"],
        drawdown
    )

    if drawdown >= MAX_DRAWDOWN:
        print(f"⛔ DRAWDOWN LIMIT: {drawdown:.1%}")
        return False

    if account["loss_streak"] >= MAX_LOSS_STREAK:
        print(f"⛔ LOSS STREAK: {account['loss_streak']}")
        return False

    return True


def update_account(result, profit=0.0):
    """بروزرسانی حساب"""

    account["total_trades"] += 1

    if result == "WIN":
        account["loss_streak"] = 0
        account["win_streak"] += 1
        account["total_wins"] += 1
        account["balance"] += profit
        account["equity"] += profit
    else:
        account["loss_streak"] += 1
        account["win_streak"] = 0
        account["total_losses"] += 1
        account["balance"] -= abs(profit)
        account["equity"] -= abs(profit)

    # بروزرسانی اوج بالانس
    account["peak_balance"] = max(
        account["peak_balance"],
        account["balance"]
    )


def position_size(confidence, price):
    """محاسبه حجم پوزیشن هوشمند"""

    base_risk = confidence / 100

    # کاهش ریسک بعد از ضررهای متوالی
    if account["loss_streak"] >= 3:
        base_risk *= 0.5
    elif account["loss_streak"] >= 2:
        base_risk *= 0.7

    # افزایش ریسک بعد از بردهای متوالی (محتاطانه)
    if account["win_streak"] >= 3:
        base_risk *= 1.1

    risk = max(MIN_RISK_PER_TRADE, min(base_risk, MAX_RISK_PER_TRADE))

    # محاسبه حجم بر اساس بالانس
    position_value = account["balance"] * risk

    if price > 0:
        quantity = position_value / price
        return round(quantity, 6)

    return 0.01


def get_account_stats():
    """آمار حساب"""
    total = account["total_trades"]
    wr = (account["total_wins"] / total * 100) if total > 0 else 0

    return {
        "balance": round(account["balance"], 2),
        "equity": round(account["equity"], 2),
        "total_trades": total,
        "winrate": round(wr, 1),
        "loss_streak": account["loss_streak"],
        "max_drawdown": round(account["max_drawdown_seen"] * 100, 1)
    }
