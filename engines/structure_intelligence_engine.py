"""
GSIS STRUCTURE INTELLIGENCE ENGINE v1.0

Multi-Timeframe Structure Fusion Layer

Input:
market_structure_v2

Output:
Institutional structure interpretation
"""


from core.database import Database
from core.logger import Logger



class StructureIntelligenceEngine:


    def __init__(self):

        self.db = Database()

        self.logger = Logger(
            "STRUCTURE_INTELLIGENCE"
        )



    def get_structure(self,symbol,timeframe):


        rows = self.db.fetch_all("""

        SELECT *

        FROM market_structure_v2

        WHERE symbol=?

        AND timeframe=?

        ORDER BY timestamp DESC

        LIMIT 1

        """,
        (
            symbol,
            timeframe
        ))


        if rows:

            return dict(rows[0])


        return None



    def score_state(self,state):


        if state == "BULLISH":

            return 1


        if state == "BEARISH":

            return -1


        return 0



    def analyze(self,symbol):


        htf = {}

        ltf = {}


        for tf in [
            "D1",
            "H4",
            "H1"
        ]:

            data=self.get_structure(
                symbol,
                tf
            )

            if data:

                htf[tf]=data



        for tf in [
            "M15",
            "M5",
            "M1"
        ]:

            data=self.get_structure(
                symbol,
                tf
            )

            if data:

                ltf[tf]=data




        htf_score=0

        htf_count=0


        for data in htf.values():

            htf_score += self.score_state(
                data["structure_state"]
            )

            htf_count += 1



        ltf_score=0

        ltf_count=0


        for data in ltf.values():

            ltf_score += self.score_state(
                data["structure_state"]
            )

            ltf_count += 1



        if htf_count:

            htf_score /= htf_count


        if ltf_count:

            ltf_score /= ltf_count




        alignment = (
            (htf_score + ltf_score + 2)
            / 4
        )



        if ltf_score > 0.3:

            execution_bias="BULLISH"

        elif ltf_score < -0.3:

            execution_bias="BEARISH"

        else:

            execution_bias="NEUTRAL"




        if htf_score > 0.3:

            macro_bias="BULLISH"

        elif htf_score < -0.3:

            macro_bias="BEARISH"

        else:

            macro_bias="RANGE"




        if alignment >=0.75:

            quality="HIGH"

        elif alignment >=0.5:

            quality="MEDIUM"

        else:

            quality="LOW"



        result={

            "symbol":symbol,

            "macro_bias":macro_bias,

            "execution_bias":execution_bias,

            "htf_score":round(htf_score,3),

            "ltf_score":round(ltf_score,3),

            "alignment":round(alignment,3),

            "quality":quality,

            "htf_structure":htf,

            "ltf_structure":ltf

        }


        return result





def run():


    engine=StructureIntelligenceEngine()


    for symbol in [

        "BTCUSDT",

        "ETHUSDT",

        "XAUTUSDT"

    ]:


        print(
            engine.analyze(symbol)
        )




if __name__=="__main__":


    print("===============================")

    print("GSIS STRUCTURE INTELLIGENCE")

    print("VERSION 1.0")

    print("===============================")


    run()


    print("===============================")

    print("STRUCTURE INTELLIGENCE COMPLETE")

    print("===============================")
