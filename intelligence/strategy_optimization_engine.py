import json
import os
import datetime


class StrategyOptimizationEngine:

    def __init__(self):

        self.file = "data/gsis_outcome_memory.json"

        print("==============================")
        print("GSIS STRATEGY OPTIMIZATION ENGINE v1.0 ONLINE")
        print("ADAPTIVE STRATEGY INTELLIGENCE ACTIVE")
        print("==============================")


    def optimize(self):

        if not os.path.exists(self.file):

            return {
                "status":"NO MEMORY FOUND"
            }


        with open(self.file,"r") as f:

            memory=json.load(f)


        total=len(memory)

        wins=0
        losses=0


        for trade in memory:

            result=trade.get(
                "result",
                "OPEN"
            )

            if result=="WIN":
                wins+=1

            elif result=="LOSS":
                losses+=1



        closed=wins+losses


        if closed > 0:

            win_rate=round(
                (wins/closed)*100,
                2
            )

        else:

            win_rate=0



        if win_rate >= 70:

            strategy_status="STRATEGY STRONG"

            adjustment="INCREASE CONFIDENCE"

        elif win_rate >= 50:

            strategy_status="STRATEGY STABLE"

            adjustment="MAINTAIN CONFIDENCE"

        else:

            strategy_status="STRATEGY WEAK"

            adjustment="REDUCE CONFIDENCE"



        result={

            "status":
            "OPTIMIZATION COMPLETE",

            "total_memory":
            total,

            "wins":
            wins,

            "losses":
            losses,

            "win_rate":
            win_rate,

            "strategy_status":
            strategy_status,

            "recommended_action":
            adjustment,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS OPTIMIZATION RESULT")
        print("==============================")
        print(result)


        return result



if __name__=="__main__":

    engine=StrategyOptimizationEngine()

    engine.optimize()
