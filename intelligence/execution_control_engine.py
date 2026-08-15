import sys
import os
from datetime import datetime, timezone


# ==========================================
# GSIS PROJECT PATH
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


print("==============================")
print("GSIS EXECUTION CONTROL ENGINE v1.1 ONLINE")
print("==============================")
print("TRADE ID + EXECUTION AUTHORIZATION ACTIVE")
print("==============================")


class ExecutionControlEngine:


    def __init__(self):

        self.execution_counter = 0


    def generate_execution_id(self):

        self.execution_counter += 1

        timestamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%d%H%M%S"
        )

        execution_id = (
            "EXEC-"
            + timestamp
            + "-"
            + str(self.execution_counter).zfill(6)
        )

        return execution_id



    def validate_trade(
        self,
        trade
    ):

        required = [
            "trade_id",
            "symbol",
            "direction",
            "entry",
            "stop_loss",
            "take_profit"
        ]


        for item in required:

            if item not in trade:

                return {

                    "status": "REJECTED",

                    "reason":
                    f"MISSING {item.upper()}"

                }


        return {

            "status": "VALIDATED",

            "message":
            "TRADE PARAMETERS ACCEPTED"

        }



    def authorize_execution(
        self,
        trade
    ):


        validation = self.validate_trade(
            trade
        )


        if validation["status"] != "VALIDATED":

            return validation



        execution_id = (
            self.generate_execution_id()
        )


        result = {


            "execution_id":
            execution_id,


            "trade_id":
            trade["trade_id"],


            "status":
            "EXECUTION AUTHORIZED",


            "symbol":
            trade["symbol"],


            "direction":
            trade["direction"],


            "entry":
            trade["entry"],


            "stop_loss":
            trade["stop_loss"],


            "take_profit":
            trade["take_profit"],


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()


        }


        print("==============================")
        print("GSIS EXECUTION AUTHORIZATION")
        print("==============================")

        print(result)


        return result



# ==========================================
# TEST MODE
# ==========================================

if __name__ == "__main__":


    engine = ExecutionControlEngine()


    test_trade = {


        "trade_id":
        "GSIS-20260728151049-000001",


        "symbol":
        "XAUUSD",


        "direction":
        "SELL",


        "entry":
        2387.5,


        "stop_loss":
        2387.8,


        "take_profit":
        2387.2

    }


    engine.authorize_execution(
        test_trade
    )
