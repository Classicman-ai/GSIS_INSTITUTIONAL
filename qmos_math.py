import math
import statistics


# ==========================================
# SIMPLE MOVING AVERAGE
# ==========================================

def sma(data):

    if len(data) == 0:
        return 0

    return sum(data) / len(data)


# ==========================================
# EXPONENTIAL MOVING AVERAGE
# ==========================================

def ema(data, period):

    if len(data) < period:
        return None

    multiplier = 2 / (period + 1)

    value = sum(data[:period]) / period

    for price in data[period:]:

        value = (
            (price - value)
            * multiplier
            + value
        )

    return value


# ==========================================
# PERCENT RETURN
# ==========================================

def percent_return(previous, current):

    if previous == 0:
        return 0

    return (
        (current - previous)
        / previous
    ) * 100


# ==========================================
# LOG RETURN
# ==========================================

def log_return(previous, current):

    if previous <= 0:
        return 0

    return math.log(current / previous)


# ==========================================
# STANDARD DEVIATION
# ==========================================

def std(data):

    if len(data) < 2:
        return 0

    return statistics.stdev(data)


# ==========================================
# MEAN
# ==========================================

def mean(data):

    if len(data) == 0:
        return 0

    return statistics.mean(data)


# ==========================================
# Z SCORE
# ==========================================

def zscore(price, mean_price, std_dev):

    if std_dev == 0:
        return 0

    return (
        price - mean_price
    ) / std_dev


# ==========================================
# HISTORICAL VOLATILITY
# ==========================================

def volatility(returns):

    if len(returns) < 2:
        return 0

    return statistics.stdev(returns)


# ==========================================
# PRICE SLOPE
# ==========================================

def slope(data):

    if len(data) < 2:
        return 0

    return data[-1] - data[0]


# ==========================================
# TREND STRENGTH
# ==========================================

def trend_strength(ema20, ema50, ema200):

    if None in (ema20, ema50, ema200):
        return 0

    score = 0

    if ema20 > ema50:
        score += 1

    if ema50 > ema200:
        score += 1

    if ema20 > ema200:
        score += 1

    return score / 3
