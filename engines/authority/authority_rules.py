# ==========================================
# GSIS TRADE AUTHORITY RULES v1.0
# ==========================================

AUTHORITY_CONFIG = {

    "authority_version": "GSIS_AUTHORITY_v1.0",

    # Minimum probability required
    "minimum_confidence": 88,

    # Entry timeframe
    "entry_timeframe": "M15",

    # Only one trade allowed
    "maximum_active_trades": 1,

    # Minimum setup
    "minimum_setup": "A+",

    # Capital protection
    "move_sl_to_be_after_tp1": True,

    # Emergency protection
    "emergency_exit": True
}


def get_rules():
    return AUTHORITY_CONFIG
