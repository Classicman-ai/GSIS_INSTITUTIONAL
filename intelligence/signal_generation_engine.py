"""
=========================================================
GSIS INSTITUTIONAL

SIGNAL GENERATION INTELLIGENCE ENGINE

Version 1.0

Institutional Trading Signal Creator

=========================================================
"""


from datetime import datetime



class SignalGenerationEngine:



    def __init__(self):

        self.name = "Signal Generation Engine"

        self.status = "CREATED"

        self.signals = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("SIGNAL GENERATION ENGINE ONLINE")
        print("==============================")





    def generate(self, market_state):


        bias = market_state.get(
            "bias",
            "NEUTRAL"
        )


        score = market_state.get(
            "institutional_score",
            0
        )


        classification = market_state.get(
            "classification",
            "NO SETUP"
        )



        signal = {


            "timestamp":

            str(datetime.utcnow()),


            "direction":

            self.direction(
                bias
            ),


            "setup":

            classification,


            "confidence":

            score,


            "status":

            self.status_check(
                score,
                bias
            ),


            "reason":

            market_state.get(
                "factors",
                []
            )

        }



        self.signals.append(signal)


        return signal






    def direction(self, bias):


        if bias == "BUY BIAS":

            return "BUY"



        elif bias == "SELL BIAS":

            return "SELL"



        return "WAIT"






    def status_check(
            self,
            score,
            bias):


        if (
            score >= 75
            and
            bias != "NEUTRAL"
        ):

            return "READY FOR EXECUTION"



        elif score >= 50:

            return "MONITOR"



        return "REJECT"






    def latest(self):


        if self.signals:

            return self.signals[-1]


        return None
