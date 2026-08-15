import os
import sys
from datetime import datetime, timezone


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


from intelligence.memory.gsis_intelligence_memory_connector import (
    GSISIntelligenceMemoryConnector
)



print("==============================")
print("GSIS ADAPTIVE INTELLIGENCE BRIDGE v1.0 ONLINE")
print("MEMORY ENHANCED DECISION INTELLIGENCE ACTIVE")
print("==============================")



class GSISAdaptiveIntelligenceBridge:


    def __init__(self):

        self.memory = GSISIntelligenceMemoryConnector()



    def analyze(
        self,
        intelligence_result,
        pattern=None
    ):


        memory_profile = self.memory.build_intelligence_profile(
            pattern
        )


        technical_confidence = intelligence_result.get(
            "confidence",
            0
        )


        historical_probability = memory_profile.get(
            "historical_probability",
            0
        )


        sample_count = memory_profile.get(
            "historical_samples",
            0
        )



        memory_bonus = 0


        if sample_count > 0:


            if historical_probability >= 80:

                memory_bonus = 10


            elif historical_probability >= 60:

                memory_bonus = 5



        adaptive_confidence = (

            technical_confidence
            +
            memory_bonus

        )


        if adaptive_confidence > 100:

            adaptive_confidence = 100



        if adaptive_confidence >= 80:

            quality = "HIGH"


        elif adaptive_confidence >= 60:

            quality = "MEDIUM"


        else:

            quality = "LOW"



        result = {


            "status":
            "ADAPTIVE INTELLIGENCE COMPLETE",


            "technical_confidence":
            technical_confidence,


            "historical_probability":
            historical_probability,


            "memory_samples":
            sample_count,


            "memory_bonus":
            memory_bonus,


            "final_confidence":
            round(
                adaptive_confidence,
                2
            ),


            "quality":
            quality,


            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()

        }



        print("==============================")
        print("GSIS ADAPTIVE INTELLIGENCE RESULT")
        print("==============================")
        print(result)


        return result





if __name__ == "__main__":


    engine = GSISAdaptiveIntelligenceBridge()


    test_intelligence = {

        "confidence":
        64.8

    }


    result = engine.analyze(

        test_intelligence,

        "BULLISH_CANDLE"

    )


    print(result)
