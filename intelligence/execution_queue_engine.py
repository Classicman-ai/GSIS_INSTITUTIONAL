from datetime import datetime, timezone


class ExecutionQueueEngine:


    def __init__(self):

        print("==============================")
        print("GSIS EXECUTION QUEUE ENGINE v2.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL ORDER CONTROL ACTIVE")
        print("==============================")

        self.queue = []


    def submit(
        self,
        trade_plan,
        risk_result,
        position_result
    ):


        print("==============================")
        print("GSIS EXECUTION VALIDATION")
        print("==============================")


        if trade_plan["status"] != "READY":

            return {
                "status":"REJECTED",
                "reason":"TRADE PLAN NOT READY"
            }


        if risk_result["status"] != "APPROVED":

            return {
                "status":"REJECTED",
                "reason":"RISK NOT APPROVED"
            }


        if position_result["status"] != "APPROVED":

            return {
                "status":"REJECTED",
                "reason":"POSITION SIZE NOT APPROVED"
            }



        order = {

            "ticket":
            len(self.queue)+1,

            "symbol":
            trade_plan["symbol"],

            "direction":
            trade_plan["direction"],

            "entry":
            trade_plan["entry"],

            "stop_loss":
            trade_plan["stop_loss"],

            "tp1":
            trade_plan["tp1"],

            "tp2":
            trade_plan["tp2"],

            "tp3":
            trade_plan["tp3"],

            "lot_size":
            position_result["lot_size"],

            "status":
            "QUEUED",

            "timestamp":
            datetime.now(timezone.utc).isoformat()

        }


        self.queue.append(order)


        print("==============================")
        print("ORDER QUEUED")
        print("==============================")

        print(order)


        return order
