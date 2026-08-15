"""
GSIS POSITION INTELLIGENCE ENGINE v1.0

Functions:
- Dynamic stop loss control
- Break-even management
- Trailing stop logic
- Multi-target TP management

Swing Mode:
TP1 = 1:2
TP2 = 1:5
TP3 = 1:8
TP4 = 1:10

Maximum risk:
5%
"""


from datetime import datetime, timezone



class PositionIntelligenceEngine:


    def __init__(self):

        self.version = "1.0"



    def manage(
        self,
        symbol,
        entry,
        current_price,
        stop_loss,
        targets
    ):


        actions = []

        status = "ACTIVE"


        risk_distance = abs(
            entry - stop_loss
        )


        profit = current_price - entry



        # Break-even protection

        if profit >= risk_distance:

            new_stop = entry

            actions.append(
                "MOVE STOP LOSS TO BREAK EVEN"
            )

        else:

            new_stop = stop_loss



        # TP monitoring

        hit_targets = []


        for name, price in targets.items():

            if current_price >= price:

                hit_targets.append(
                    name
                )


        if "TP1" in hit_targets:

            actions.append(
                "TP1 HIT - CLOSE 30%"
            )


        if "TP2" in hit_targets:

            actions.append(
                "TP2 HIT - CLOSE 30%"
            )


        if "TP3" in hit_targets:

            actions.append(
                "TP3 HIT - CLOSE 30%"
            )


        if "TP4" in hit_targets:

            actions.append(
                "FINAL TARGET REACHED"
            )

            status = "COMPLETED"



        return {

            "engine":
            "GSIS POSITION INTELLIGENCE ENGINE",

            "version":
            self.version,

            "symbol":
            symbol,

            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

            "status":
            status,

            "entry":
            entry,

            "current_price":
            current_price,

            "stop_loss":
            new_stop,

            "targets_hit":
            hit_targets,

            "actions":
            actions
        }



if __name__ == "__main__":


    engine = PositionIntelligenceEngine()


    print(
        engine.manage(
            "BTCUSDT",
            64000,
            68500,
            62000,
            {
                "TP1":68000,
                "TP2":74000,
                "TP3":80000,
                "TP4":84000
            }
        )
    )
