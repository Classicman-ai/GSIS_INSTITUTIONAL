"""
=========================================================

GSIS INSTITUTIONAL

CAPITAL MANAGEMENT ENGINE v1.0

Institutional Money Management Layer

=========================================================
"""


import os
import sys

from datetime import datetime, UTC


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from core.event_bus import event_bus



class CapitalManagementEngine:


    def __init__(self):

        self.account_balance = 100000

        self.risk_percent = 1.0


        print("==============================")
        print("GSIS CAPITAL MANAGEMENT ENGINE v1.0 ONLINE")
        print("==============================")
        print("INSTITUTIONAL MONEY MANAGEMENT ACTIVE")
        print("==============================")


    def calculate(self, execution):


        print()

        print("==============================")
        print("GSIS CAPITAL ANALYSIS")
        print("==============================")


        print("EXECUTION INPUT:")
        print(execution)



        symbol = execution.get(
            "symbol",
            "UNKNOWN"
        )



        if execution.get(
            "execution_status"
        ) != "QUEUED":


            result = {

                "symbol": symbol,

                "capital_status":
                "NOT_APPROVED",

                "reason":
                "Execution not approved",

                "timestamp":
                datetime.now(
                    UTC
                ).isoformat()

            }


        else:


            risk_amount = (

                self.account_balance

                *

                self.risk_percent

                /

                100

            )


            result = {

                "symbol": symbol,

                "capital_status":
                "READY",

                "account_balance":
                self.account_balance,

                "risk_percent":
                self.risk_percent,

                "risk_amount":
                risk_amount,

                "mode":
                "SIMULATION",

                "timestamp":
                datetime.now(
                    UTC
                ).isoformat()

            }



        print()

        print("CAPITAL RESULT:")
        print(result)



        event_bus.publish(

            "capital_analysis",

            result

        )




engine = CapitalManagementEngine()



event_bus.subscribe(

    "execution_queue",

    engine.calculate

)



def capital_listener(data):


    print()

    print(
        "CAPITAL EVENT RECEIVED"
    )

    print(data)




event_bus.subscribe(

    "capital_analysis",

    capital_listener

)
