import datetime



class GSISConfidenceCalibrationEngine:


    def __init__(self):

        print("==============================")
        print("GSIS CONFIDENCE CALIBRATION ENGINE v2.0 ONLINE")
        print("ADAPTIVE CONFIDENCE OPTIMIZATION ACTIVE")
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



        historical_component = (

            historical_probability

            *

            reliability

        )



        confidence = (

            (technical_score * 0.50)

            +

            (historical_component * 0.30)

            +

            (liquidity_score * 0.20)

            -

            (economic_risk * 0.05)

        )



        # Strong technical + strong history protection

        if (

            technical_score >= 80

            and

            historical_probability >= 80

        ):

            confidence += 10



        # Cap score

        confidence = min(
            confidence,
            100
        )



        if confidence >= 85:

            quality = "INSTITUTIONAL"

        elif confidence >= 75:

            quality = "HIGH"

        elif confidence >= 55:

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
                confidence,
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

            return 0.5


        elif samples >= 3:

            return 0.4


        else:

            return 0.25




if __name__ == "__main__":


    engine = GSISConfidenceCalibrationEngine()


    print(
        engine.calculate(
            85,
            100,
            3,
            80,
            0
        )
    )
