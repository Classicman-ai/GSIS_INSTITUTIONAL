"""
GSIS GLOBAL RISK CONFIGURATION
Version: 1.0
"""

# Trading Mode
TRADING_MODE = "SWING"

# Risk Management
MAX_RISK_PER_TRADE = 0.05      # 5%
MIN_RISK_REWARD = 2            # 1:2
MAX_RISK_REWARD = 10           # 1:10

# Take Profit Levels
TP_LEVELS = {
    "TP1": {
        "rr": 2,
        "close_percent": 30
    },
    "TP2": {
        "rr": 5,
        "close_percent": 30
    },
    "TP3": {
        "rr": 8,
        "close_percent": 25
    },
    "TP4": {
        "rr": 10,
        "close_percent": 15
    }
}

# Stop Loss Rules
MOVE_TO_BREAK_EVEN_AFTER = "TP1"
ENABLE_TRAILING_STOP = True

# Position Rules
MAX_OPEN_TRADES = 3
ALLOW_PARTIAL_CLOSE = True
ALLOW_MULTIPLE_POSITIONS = False
