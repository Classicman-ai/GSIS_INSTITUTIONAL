from datetime import datetime, timezone


class TradeMonitorEngine:

    def __init__(self):
        print("==============================")
        print("GSIS TRADE MONITOR ENGINE v1.1 ONLINE")
        print("AUTONOMOUS TRADE STATUS TRACKING ACTIVE")
        print("==============================")


    def update_status(self, trade):

        result={

            "trade_id":trade.get("trade_id"),

            "status":"RUNNING",

            "current_price":trade.get("entry"),

            "profit_loss":0,

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }

        print("==============================")
        print("GSIS TRADE STATUS UPDATE")
        print("==============================")
        print(result)

        return result


    monitor_trade = update_status
    check_trade = update_status
