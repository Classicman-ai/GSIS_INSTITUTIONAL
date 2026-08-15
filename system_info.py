# ==========================================
# QMOS SYSTEM INFORMATION
# ==========================================

SYSTEM_NAME = "QMOS"
SYSTEM_VERSION = "0.1.0"

BUILD = "Institutional Research Edition"

DATABASE_VERSION = "1.0"

AUTHOR = "Khamis"

# ==========================================
# MARKET CONFIGURATION
# ==========================================

ASSETS = [
    "XAUTUSDT",
    "BTCUSDT",
    "ETHUSDT"
]

TIMEFRAMES = {
    "M1": "1m",
    "M5": "5m",
    "M15": "15m",
    "H1": "1h",
    "H4": "4h",
    "D1": "1d",
    "W1": "1w",
    "MN1": "1M"
}

# ==========================================
# ENGINE STATUS
# ==========================================

ENGINES = {
    "Engine01": "Data Feed",
    "Engine02": "Candle Builder",
    "Engine03": "Storage",
    "Engine04": "Validation",
    "Engine05": "Statistics",
    "Engine06": "Market Regime"
}
