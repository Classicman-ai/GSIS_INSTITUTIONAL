import datetime


VALID_EVENTS = [
    "TRADE_OPENED",
    "TP1_HIT",
    "TP2_HIT",
    "TP3_HIT",
    "TP4_HIT",
    "STOP_MOVED_BREAK_EVEN",
    "TRAILING_STOP_ACTIVE",
    "TRADE_COMPLETED",
    "TRADE_FAILED"
]


def validate_event(event):

    required = [
        "trade_id",
        "symbol",
        "event"
    ]

    for field in required:
        if field not in event:
            return False

    if event["event"] not in VALID_EVENTS:
        return False

    return True


def timestamp():

    return datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat()
