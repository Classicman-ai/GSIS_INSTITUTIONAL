"""
=========================================================
GSIS INSTITUTIONAL
Pattern Discovery Engine
Version: 1.0
=========================================================
"""

import sqlite3

from database.pattern_database import PatternDatabase


class PatternDiscovery:


    def __init__(self):

        self.history_db = (
            "database/historical.db"
        )

        self.pattern_db = PatternDatabase()



    def connect_history(self):

        return sqlite3.connect(
            self.history_db
        )



    def load_candles(
            self,
            symbol,
            timeframe,
            limit=1000):


        conn = self.connect_history()

        cursor = conn.cursor()


        cursor.execute("""
        SELECT *

        FROM candles

        WHERE symbol=?
        AND timeframe=?

        ORDER BY timestamp ASC

        LIMIT ?

        """,

        (
            symbol,
            timeframe,
            limit
        ))


        candles = cursor.fetchall()


        conn.close()


        return candles



    def analyze_candle_structure(
            self,
            candles):


        patterns = []


        for i in range(
            2,
            len(candles)
        ):

            previous = candles[i-2]

            current = candles[i]


            # Simple first pattern logic
            # Future versions will add
            # SMC, liquidity, volume,
            # regime analysis.


            if current[5] > previous[5]:

                patterns.append(

                {

                "type":
                "Bullish Continuation",

                "conditions":
                {

                "previous_close":
                previous[5],

                "current_close":
                current[5]

                }

                }

                )


        return patterns



    def discover(
            self,
            symbol,
            timeframe):


        candles = self.load_candles(
            symbol,
            timeframe
        )


        found = self.analyze_candle_structure(
            candles
        )


        print(
            "PATTERNS FOUND:",
            len(found)
        )


        return found
