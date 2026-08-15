"""
GSIS TRADE MANAGEMENT ENGINE v2.0

Swing Trade Lifecycle Manager

Features:
- TP1 TP2 TP3 TP4 management
- Partial exits
- Breakeven protection
- Trailing stop
- Fusion reversal protection
"""


from datetime import datetime, timezone



class TradeManagementEngine:


    def __init__(self):

        self.version = "2.0"



    def manage(
        self,
        symbol,
        execution,
        current_price
    ):


        status = execution.get(
            "status",
            "UNKNOWN"
        )


        if status != "READY_FOR_EXECUTION":

            return {

                "engine":
                "GSIS TRADE MANAGEMENT ENGINE",

                "version":
                self.version,

                "symbol":
                symbol,

                "status":
                "WAITING",

                "reason":
                "NO ACTIVE TRADE"

            }



        tp = execution.get(
            "take_profit",
            {}
        )


        actions = []


        actions.append(
            "MONITOR POSITION"
        )


        if current_price >= tp.get("TP1",0):

            actions.append(
                "TP1 HIT - CLOSE 30%"
            )

            actions.append(
                "MOVE STOP LOSS TO BREAKEVEN"
            )



        if current_price >= tp.get("TP2",0):

            actions.append(
                "TP2 HIT - CLOSE 30%"
            )

            actions.append(
                "ACTIVATE TRAILING STOP"
            )



        if current_price >= tp.get("TP3",0):

            actions.append(
                "TP3 HIT - CLOSE 30%"
            )



        if current_price >= tp.get("TP4",0):

            actions.append(
                "TP4 HIT - CLOSE FINAL RUNNER"
            )



        return {


            "engine":
            "GSIS TRADE MANAGEMENT ENGINE",


            "version":
            self.version,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "symbol":
            symbol,


            "status":
            "ACTIVE",


            "current_price":
            current_price,


            "actions":
            actions

        }



if __name__ == "__main__":


    engine = TradeManagementEngine()


    print(
        "==============================="
    )

    print(
        "GSIS TRADE MANAGEMENT ENGINE v2.0"
    )

    print(
        "==============================="
    )
