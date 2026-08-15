import datetime


class PositionIntelligenceEngine:

    def __init__(self):

        print("==============================")
        print("GSIS POSITION INTELLIGENCE ENGINE v1.0 ONLINE")
        print("ENTRY QUALITY CONTROL ACTIVE")
        print("==============================")


    def evaluate(
        self,
        direction,
        entry,
        stop_loss,
        take_profit
    ):

        reasons = []
        score = 0


        if direction in ["BUY", "SELL"]:

            score += 20
            reasons.append(
                "DIRECTION VALID"
            )

        else:

            reasons.append(
                "INVALID DIRECTION"
            )


        if direction == "SELL":

            risk = stop_loss - entry
            reward = entry - take_profit

        else:

            risk = entry - stop_loss
            reward = take_profit - entry



        if risk > 0:

            score += 25
            reasons.append(
                "STOP LOSS VALID"
            )

        else:

            reasons.append(
                "STOP LOSS INVALID"
            )


        if reward > 0:

            score += 25
            reasons.append(
                "TAKE PROFIT VALID"
            )

        else:

            reasons.append(
                "TAKE PROFIT INVALID"
            )


        if risk > 0:

            reward_ratio = round(
                reward / risk,
                2
            )

        else:

            reward_ratio = 0



        if reward_ratio >= 1.5:

            score += 30
            reasons.append(
                "REWARD RISK ACCEPTABLE"
            )

        else:

            reasons.append(
                "REWARD RISK WEAK"
            )



        if score >= 80:

            status = "POSITION APPROVED"

        elif score >= 50:

            status = "POSITION CAUTION"

        else:

            status = "POSITION BLOCKED"



        result = {

            "status":
                status,

            "position_score":
                score,

            "direction":
                direction,

            "entry":
                entry,

            "stop_loss":
                stop_loss,

            "take_profit":
                take_profit,

            "reward_risk":
                reward_ratio,

            "reasons":
                reasons,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS POSITION RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = PositionIntelligenceEngine()


    engine.evaluate(

        direction="SELL",

        entry=2387.5,

        stop_loss=2387.8,

        take_profit=2386.6

    )
