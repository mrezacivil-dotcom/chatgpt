# =========================
# V60 FULL AI RISK ENGINE
# =========================

account = {
    "balance": 1000.0,
    "equity": 1000.0,
    "loss_streak": 0,
    "max_drawdown": 0.0
}


# =========================
# POSITION SIZE
# =========================

def position_size(confidence, volatility):

    base_risk = 0.01  # 1%

    conf_factor = confidence / 100.0

    vol_factor = 1.0 - (volatility * 8)
    vol_factor = max(0.4, min(vol_factor, 1.0))

    risk = base_risk * conf_factor * vol_factor

    return max(0.002, min(risk, 0.02))


# =========================
# KILL SWITCH SYSTEM
# =========================

def trading_allowed():

    # drawdown protection
    drawdown = (account["balance"] - account["equity"]) / account["balance"]

    if drawdown >= 0.15:
        print("⛔ KILL SWITCH: DRAWDOWN LIMIT HIT")
        return False

    # loss streak protection
    if account["loss_streak"] >= 5:
        print("⛔ KILL SWITCH: LOSS STREAK LIMIT HIT")
        return False

    return True


# =========================
# UPDATE ACCOUNT AFTER TRADE
# =========================

def update_account(pnl):

    account["equity"] += pnl

    if pnl < 0:
        account["loss_streak"] += 1
    else:
        account["loss_streak"] = 0

    # track max drawdown
    dd = (account["balance"] - account["equity"]) / account["balance"]
    account["max_drawdown"] = max(account["max_drawdown"], dd)
