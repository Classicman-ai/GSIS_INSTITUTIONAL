import datetime


class GSISIntelligencePipelineController:

    def __init__(self):

        print("==============================")
        print("GSIS INTELLIGENCE PIPELINE CONTROLLER v1.0 ONLINE")
        print("FULL INTELLIGENCE PIPELINE CONTROL ACTIVE")
        print("==============================")


    def run(

        self,

        market_data,

        engines

    ):


        print("==============================")
        print("GSIS PIPELINE EXECUTION START")
        print("==============================")


        structure = engines["structure"].analyze(
            market_data
        )


        zone = engines["zone"].analyze(
            market_data
        )


        liquidity = engines["liquidity"].analyze(
            market_data
        )


        candlestick = engines["candlestick"].analyze(
            market_data
        )


        chart_pattern = engines["chart"].analyze(
            market_data
        )


        economic = engines["economic"].analyze()


        historical = engines["probability"].analyze_pattern(
            "BEARISH_ENGULFING"
        )


        historical_probability = (

            historical.get(
                "win_probability",
                0
            )

        )


        calibration = engines["calibration"].calculate(

            technical_score=90,

            historical_probability=
            historical_probability,

            sample_size=
            historical.get(
                "samples",
                0
            ),

            liquidity_score=85,

            economic_risk=10

        )


        fusion = engines["fusion"].analyze(

            structure,

            zone,

            liquidity,

            candlestick,

            chart_pattern,

            economic,

            historical_probability,

            calibration["final_confidence"]

        )


        result = {


            "status":

            "PIPELINE COMPLETE",


            "decision":

            fusion,


            "timestamp":

            datetime.datetime.now(

                datetime.timezone.utc

            ).isoformat()


        }


        print("==============================")
        print("GSIS PIPELINE RESULT")
        print("==============================")

        print(result)


        return result



if __name__ == "__main__":

    print(
        "Pipeline controller ready."
    )
