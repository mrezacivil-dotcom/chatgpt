account = {
    "balance": 1000,
    "equity": 1000,
    "loss_streak": 0,
    "max_drawdown": 0
}


def trading_allowed():

    drawdown = (
        account["balance"] -
        account["equity"]
    ) / account["balance"]

    if drawdown >= 0.15:
        print("⛔ DRAWDOWN LIMIT")
        return False

    if account["loss_streak"] >= 5:
        print("⛔ LOSS STREAK LIMIT")
        return False

    return True


def update_account(result):

    if result == "LOSS":
        account["loss_streak"] += 1
    else:
        account["loss_streak"] = 0


def position_size(confidence):

    risk = confidence / 100

    return max(0.01, min(risk, 0.03))
