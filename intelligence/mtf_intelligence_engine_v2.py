"""
=========================================================
GSIS INSTITUTIONAL

MULTI TIMEFRAME INTELLIGENCE ENGINE

Version 2.0

HTF Bias + LTF Execution Alignment

=========================================================
"""


from datetime import datetime



class MTFIntelligenceEngineV2:


    def __init__(self):

        self.name = "MTF Intelligence Engine v2"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("MTF INTELLIGENCE ENGINE v2 ONLINE")
        print("==============================")





    def analyze(self, data):


        htf = data.get(
            "higher_timeframe",
            {}
        )


        ltf = data.get(
            "lower_timeframe",
            {}
        )



        htf_bias = htf.get(
            "bias",
            "NEUTRAL"
        )


        ltf_bias = ltf.get(
            "bias",
            "NEUTRAL"
        )



        alignment = self.check_alignment(
            htf_bias,
            ltf_bias
        )


        confidence = self.calculate_confidence(
            alignment
        )



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "htf_bias":

            htf_bias,


            "ltf_bias":

            ltf_bias,


            "alignment":

            alignment,


            "confidence":

            confidence,


            "decision":

            self.decision(
                alignment
            )

        }



        self.history.append(result)


        return result






    def check_alignment(
            self,
            htf,
            ltf):


        if htf == ltf:

            return "ALIGNED"


        if (
            htf == "BULLISH"
            and
            ltf == "BEARISH"
        ):

            return "CONFLICT"



        if (
            htf == "BEARISH"
            and
            ltf == "BULLISH"
        ):

            return "CONFLICT"



        return "NEUTRAL"






    def calculate_confidence(
            self,
            alignment):


        if alignment == "ALIGNED":

            return 85


        elif alignment == "CONFLICT":

            return 20


        return 50






    def decision(
            self,
            alignment):


        if alignment == "ALIGNED":

            return "APPROVED"



        elif alignment == "CONFLICT":

            return "WAIT"



        return "CAUTION"






    def latest(self):


        if self.history:

            return self.history[-1]


        return None
