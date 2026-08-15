import sqlite3
import os
from config import DATABASE

# Ensure database directory exists
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Assets
cursor.execute("""
CREATE TABLE IF NOT EXISTS assets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT UNIQUE
)
""")

# Candles
cursor.execute("""
CREATE TABLE IF NOT EXISTS candles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,
    timeframe TEXT,

    open_time INTEGER,

    open REAL,
    high REAL,
    low REAL,
    close REAL,

    volume REAL,

    close_time INTEGER,

    UNIQUE(symbol, timeframe, open_time)
)
""")

# Signals
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,
    timeframe TEXT,

    signal TEXT,

    confidence REAL,

    entry REAL,
    stop_loss REAL,
    take_profit REAL,

    timestamp INTEGER
)
""")

# Trades
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    symbol TEXT,

    side TEXT,

    entry REAL,
    exit REAL,

    pnl REAL,

    opened INTEGER,
    closed INTEGER
)
""")

conn.commit()

print("===================================")
print("QMOS DATABASE READY")
print(DATABASE)
print("===================================")

conn.close()
