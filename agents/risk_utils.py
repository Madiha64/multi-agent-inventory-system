agents/risk_utils.py
def get_risk_level(current_stock, forecast, reorder_threshold, safety_stock):
    if current_stock < reorder_threshold:
        return "HIGH", "🔴"
    elif current_stock < forecast + safety_stock:
        return "MEDIUM", "🟡"
    else:
        return "LOW", "🟢"