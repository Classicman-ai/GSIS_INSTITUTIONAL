"""
GSIS STRUCTURE ENGINE v3.0

Institutional Market Structure Detection

Outputs:
- Swing points
- BOS
- CHOCH
- Structure state
- Strength score

Database:
market_structure_v2
"""

from core.database import Database
from core.logger import Logger
import time



class StructureEngine:


    def __init__(self):

        self.db = Database()

        self.logger = Logger(
            "STRUCTURE_ENGINE"
        )



    def analyze(self,symbol,timeframe):


        candles = self.db.fetch_all("""


        SELECT *

        FROM candles

        WHERE symbol=?

        AND timeframe=?

        ORDER BY open_time DESC

        LIMIT 100


        """,
        (
            symbol,
            timeframe
        ))



        if len(candles) < 20:

            return None



        candles = list(reversed(candles))



        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]

        closes = [
            c["close"]
            for c in candles
        ]



        last_high=max(highs)

        last_low=min(lows)


        previous_high=max(
            highs[:-10]
        )

        previous_low=min(
            lows[:-10]
        )



        current=closes[-1]



        if current > previous_high:

            state="BULLISH"

            bos="UP"

            choch="NONE"


        elif current < previous_low:

            state="BEARISH"

            bos="DOWN"

            choch="NONE"


        else:

            state="RANGE"

            bos="NONE"

            choch="NONE"





        strength=abs(
            current -
            ((last_high+last_low)/2)
        ) / current



        self.save(

            symbol,

            timeframe,

            last_high,

            last_low,

            state,

            bos,

            choch,

            strength

        )


        return state





    def save(

        self,

        symbol,

        timeframe,

        high,

        low,

        state,

        bos,

        choch,

        strength

    ):


        self.db.execute("""


        INSERT OR REPLACE INTO market_structure_v2

        (

        symbol,

        timeframe,

        timestamp,

        swing_high,

        swing_low,

        structure_state,

        structure_break,

        change_of_character,

        last_high,

        last_low,

        structure_strength

        )


        VALUES

        (?,?,?,?,?,?,?,?,?,?,?)


        """,

        (

        symbol,

        timeframe,

        int(time.time()*1000),

        high,

        low,

        state,

        bos,

        choch,

        high,

        low,

        strength

        ))



def run():


    engine=StructureEngine()


    assets=[

        "BTCUSDT",

        "ETHUSDT",

        "XAUTUSDT"

    ]


    timeframes=[

        "M1",

        "M5",

        "M15",

        "H1",

        "H4",

        "D1"

    ]



    for asset in assets:

        for tf in timeframes:

            result=engine.analyze(
                asset,
                tf
            )

            print(
                asset,
                tf,
                result
            )



if __name__=="__main__":

    print("===============================")

    print("GSIS STRUCTURE ENGINE v3.0")

    print("INSTITUTIONAL STRUCTURE MODEL")

    print("===============================")


    run()


    print("===============================")

    print("STRUCTURE UPDATE COMPLETE")

    print("===============================")
