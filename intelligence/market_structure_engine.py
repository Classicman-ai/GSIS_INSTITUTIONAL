"""
=========================================================
GSIS INSTITUTIONAL

MARKET STRUCTURE INTELLIGENCE ENGINE (MSIE)

Version: 1.0

Functions:
- Detect BOS
- Detect CHOCH
- Classify structure
- Measure structural confidence

=========================================================
"""


from datetime import datetime
import uuid



class MarketStructureEngine:


    def __init__(self):

        self.name = "Market Structure Intelligence Engine"

        self.status = "CREATED"

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("MARKET STRUCTURE ENGINE ONLINE")
        print("==============================")



    def analyze(
            self,
            candles):


        if len(candles) < 3:

            return None



        previous = candles[-3]

        current = candles[-1]



        event = "NONE"

        direction = "NEUTRAL"

        confidence = 0



        # Bullish BOS

        if current["high"] > previous["high"]:


            event = "BOS"

            direction = "BULLISH"

            confidence += 50



        # Bearish BOS

        elif current["low"] < previous["low"]:


            event = "BOS"

            direction = "BEARISH"

            confidence += 50



        # Momentum confirmation

        if current["close"] > current["open"]:

            if direction == "BULLISH":

                confidence += 30



        elif current["close"] < current["open"]:

            if direction == "BEARISH":

                confidence += 30



        structure = self.classify(
            direction,
            confidence
        )



        result = {


            "structure_id":

            str(uuid.uuid4()),


            "timestamp":

            str(datetime.utcnow()),


            "event":

            event,


            "direction":

            direction,


            "confidence":

            min(
                confidence,
                100
            ),


            "classification":

            structure


        }


        self.history.append(result)


        return result



    def classify(
            self,
            direction,
            confidence):


        if confidence >= 80:


            if direction == "BULLISH":

                return "STRONG BULLISH STRUCTURE"


            elif direction == "BEARISH":

                return "STRONG BEARISH STRUCTURE"



        elif confidence >= 50:


            if direction == "BULLISH":

                return "BULLISH STRUCTURE"


            elif direction == "BEARISH":

                return "BEARISH STRUCTURE"



        return "NEUTRAL STRUCTURE"



    def report(self):

        return self.history
