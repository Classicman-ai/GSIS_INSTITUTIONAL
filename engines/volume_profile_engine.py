"""
GSIS ENGINE 8.2
VOLUME PROFILE INTELLIGENCE ENGINE
VERSION 1.1

Institutional Volume Distribution Analysis
Compatible with GSIS candles schema
"""

from core.logger import Logger
from core.database import Database
import time



class VolumeProfileEngine:


    engine_name = "VOLUME_PROFILE_ENGINE"
    version = "1.1"



    def __init__(self):

        self.logger = Logger(
            self.engine_name
        )

        self.db = Database()

        self.create_table()



    def create_table(self):

        self.db.execute("""

        CREATE TABLE IF NOT EXISTS volume_profile (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            timestamp INTEGER,

            poc REAL,

            vah REAL,

            val REAL,

            volume_bias TEXT,

            profile_quality TEXT

        )

        """)



    def start(self):

        self.logger.info(
            "VOLUME PROFILE ENGINE ONLINE"
        )



    def calculate(self, symbol, timeframe):


        candles = self.db.fetch_all("""

        SELECT
            high,
            low,
            close,
            volume

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



        if not candles:

            return {

                "status":"NO_DATA"

            }



        prices = []

        volumes = []



        for candle in candles:


            price = (

                candle["high"] +
                candle["low"] +
                candle["close"]

            ) / 3



            prices.append(price)

            volumes.append(
                candle["volume"]
            )



        total_volume = sum(volumes)



        if total_volume == 0:

            return {

                "status":"NO_VOLUME"

            }



        poc = (

            sum(

                p*v

                for p,v in zip(
                    prices,
                    volumes
                )

            )

            /
            total_volume

        )



        highest = max(prices)

        lowest = min(prices)



        vah = lowest + (
            (highest-lowest)
            *0.70
        )


        val = lowest + (
            (highest-lowest)
            *0.30
        )



        bias = self.get_bias(

            prices[0],

            poc

        )



        result = {


            "symbol":symbol,

            "timeframe":timeframe,

            "poc":round(poc,2),

            "vah":round(vah,2),

            "val":round(val,2),

            "volume_bias":bias,

            "profile_quality":"NORMAL"

        }



        self.save(result)



        return result




    def get_bias(self,current,poc):


        if current > poc:

            return "BUY_ACCEPTANCE"



        elif current < poc:

            return "SELL_ACCEPTANCE"



        return "BALANCED"




    def save(self,data):


        self.db.execute("""

        INSERT INTO volume_profile

        (

        symbol,
        timeframe,
        timestamp,
        poc,
        vah,
        val,
        volume_bias,
        profile_quality

        )

        VALUES (?,?,?,?,?,?,?,?)

        """,

        (

        data["symbol"],
        data["timeframe"],
        int(time.time()),
        data["poc"],
        data["vah"],
        data["val"],
        data["volume_bias"],
        data["profile_quality"]

        ))
