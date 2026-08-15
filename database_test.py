from database.database_engine import DatabaseEngine


db = DatabaseEngine()


db.initialize()


db.save_candle(
    "BTCUSDT",
    "M1",
    65000,
    65100,
    64900,
    65050,
    120
)


db.log_event(
    "Database test completed"
)


print(
    db.report()
)
