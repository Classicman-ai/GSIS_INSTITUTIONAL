import sqlite3
import datetime


class GSISHistoricalStatisticsEngine:

    def __init__(self):

        print("==============================")
        print("GSIS HISTORICAL STATISTICS ENGINE v1.0 ONLINE")
        print("PERFORMANCE ANALYTICS ACTIVE")
        print("==============================")

        self.database = "database/gsis_intelligence.db"


    def connect(self):

        return sqlite3.connect(
            self.database
        )


    def total_trades(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM market_reactions
            """
        )

        result = cursor.fetchone()[0]

        conn.close()

        return result



    def win_rate(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT

            COUNT(*)

            FROM market_reactions

            WHERE trade_result='WIN'

            """
        )

        wins = cursor.fetchone()[0]


        cursor.execute(
            """
            SELECT COUNT(*)
            FROM market_reactions
            """
        )

        total = cursor.fetchone()[0]


        conn.close()


        if total == 0:

            return 0


        return round(

            (wins / total) * 100,

            2

        )



    def average_rr(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(

            """
            SELECT AVG(rr)

            FROM market_reactions

            """

        )


        result = cursor.fetchone()[0]


        conn.close()


        if result is None:

            return 0


        return round(

            result,

            2

        )



    def analyze(self):

        result = {

            "status":
            "STATISTICS COMPLETE",

            "total_samples":
            self.total_trades(),

            "win_rate":
            self.win_rate(),

            "average_rr":
            self.average_rr(),

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }


        print("==============================")
        print("GSIS STATISTICS RESULT")
        print("==============================")
        print(result)


        return result



if __name__ == "__main__":


    engine = GSISHistoricalStatisticsEngine()

    engine.analyze()
