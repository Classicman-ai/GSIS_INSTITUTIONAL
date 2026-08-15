"""
GSIS EXECUTION CONFIGURATION
Version: 1.0
"""

# =====================================================
# EXECUTION MODE
# =====================================================

EXECUTION_MODE = "SIMULATION"      # SIMULATION | PAPER | LIVE

# =====================================================
# ORDER SETTINGS
# =====================================================

DEFAULT_ORDER_TYPE = "MARKET"

ALLOW_LONG = True
ALLOW_SHORT = True

# =====================================================
# RISK CONTROLS
# =====================================================

MAX_OPEN_TRADES = 3
MAX_PENDING_ORDERS = 5

# =====================================================
# EXECUTION PARAMETERS
# =====================================================

SLIPPAGE = 0.001
COMMISSION = 0.0005

# =====================================================
# POSITION MANAGEMENT
# =====================================================

ENABLE_BREAK_EVEN = True
ENABLE_TRAILING_STOP = True

BREAK_EVEN_AFTER = "TP1"
TRAIL_AFTER = "TP2"

# =====================================================
# EXECUTION SAFETY
# =====================================================

TIMEOUT_SECONDS = 30
RETRY_COUNT = 3

# =====================================================
# LOGGING
# =====================================================

SAVE_EXECUTION_LOG = True
SAVE_TRADE_HISTORY = True
