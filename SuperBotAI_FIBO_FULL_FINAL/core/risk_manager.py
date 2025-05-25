
def calculate_position_size(capital, risk_percent, entry, stop, leverage=1):
    risk_amount = capital * risk_percent / 100
    diff = abs(entry - stop)
    if diff == 0:
        return 0
    size = (risk_amount / diff) * leverage
    return round(size, 2)
