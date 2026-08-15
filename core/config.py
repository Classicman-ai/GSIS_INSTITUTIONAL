"""
GSIS CORE CONFIGURATION
VERSION 1.0

Central system configuration
"""

import os


# ===============================
# DATABASE
# ===============================

DATABASE_PATH = "database/qmos.db"



# ===============================
# SYSTEM INFORMATION
# ===============================

SYSTEM_NAME = "GSIS"

SYSTEM_VERSION = "2.0"

ENVIRONMENT = "RESEARCH"



# ===============================
# SUPPORTED ASSETS
# ===============================

ASSETS = [

    "XAUTUSDT",
    "BTCUSDT",
    "ETHUSDT"

]



# ===============================
# TIMEFRAME MATRIX
# ===============================

TIMEFRAMES = [

    "M1",
    "M5",
    "M15",
    "H1",
    "H4",
    "D1",
    "W1",
    "MN1"

]



# ===============================
# ENGINE REGISTRY
# ===============================

ENGINES = {

    "ENGINE_01": "DATA",

    "ENGINE_05": "STATISTICS",

    "ENGINE_06": "REGIME",

    "ENGINE_07": "STRUCTURE",

    "ENGINE_07.5": "INTELLIGENCE",

    "ENGINE_07.6": "MODEL",

    "ENGINE_07.7": "CONFIDENCE",

    "ENGINE_07.8": "MEMORY",

    "ENGINE_08": "LIQUIDITY"

}



# ===============================
# DIRECTORIES
# ===============================

BASE_DIR = os.getcwd()

LOG_DIR = "logs"

DATABASE_DIR = "database"



# ===============================
# TEST
# ===============================

if __name__ == "__main__":

    print("===================================")
    print("GSIS CORE CONFIGURATION")
    print("VERSION:", SYSTEM_VERSION)
    print("===================================")

    print("Assets:")

    for asset in ASSETS:
        print("-", asset)


    print("\nTimeframes:")

    for tf in TIMEFRAMES:
        print("-", tf)


    print("\nConfiguration Ready")
