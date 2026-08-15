import datetime


class GSISConfidenceCalibrationEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CONFIDENCE CALIBRATION ENGINE v1.0 ONLINE")
        print("DECISION QUALITY OPTIMIZATION ACTIVE")
        print("==============================")



    def calculate(

        self,

        technical_score,

        historical_probability,

        sample_size,

        liquidity_score,

        economic_risk

    ):


        reliability = self.sample_reliability(

            sample_size

        )


        adjusted_history = (

            historical_probability

            *

            reliability

        )


        final_score = (

            (technical_score * 0.45)

            +

            (adjusted_history * 0.30)

            +

            (liquidity_score * 0.20)

            -

            (economic_risk * 0.05)

        )


        if final_score >= 85:

            quality = "INSTITUTIONAL"

        elif final_score >= 70:

            quality = "HIGH"

        elif final_score >= 50:

            quality = "MEDIUM"

        else:

            quality = "LOW"



        return {


            "status":

            "CONFIDENCE CALIBRATION COMPLETE",


            "technical_score":

            technical_score,


            "historical_probability":

            historical_probability,


            "sample_reliability":

            reliability,


            "liquidity_score":

            liquidity_score,


            "economic_risk":

            economic_risk,


            "final_confidence":

            round(

                final_score,

                2

            ),


            "quality":

            quality,


            "timestamp":

            datetime.datetime.now(

                datetime.timezone.utc

            ).isoformat()


        }



    def sample_reliability(

        self,

        samples

    ):


        if samples >= 500:

            return 1.0

        elif samples >= 100:

            return 0.8

        elif samples >= 20:

            return 0.6

        elif samples >= 5:

            return 0.4

        else:

            return 0.2




if __name__ == "__main__":


    engine = GSISConfidenceCalibrationEngine()


    result = engine.calculate(

        technical_score=90,

        historical_probability=100,

        sample_size=1,

        liquidity_score=85,

        economic_risk=10

    )


    print("==============================")
    print("GSIS CONFIDENCE RESULT")
    print("==============================")
    print(result)
