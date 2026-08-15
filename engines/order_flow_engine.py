"""
GSIS ENGINE 8.3
ORDER FLOW INTELLIGENCE ENGINE
VERSION 1.0

Institutional Flow Analysis Layer

Calculates:
- Buy/Sell pressure
- Volume delta
- Flow direction
- Absorption detection
"""

from core.logger import Logger
from core.database import Database
import time



class OrderFlowEngine:


    engine_name = "ORDER_FLOW_ENGINE"
    version = "1.0"



    def __init__(self):

        self.logger = Logger(
            self.engine_name
        )

        self.db = Database()

        self.create_table()



    def create_table(self):

        self.db.execute("""

        CREATE TABLE IF NOT EXISTS order_flow (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            timeframe TEXT,

            timestamp INTEGER,

            buy_volume REAL,

            sell_volume REAL,

            delta REAL,

            flow_bias TEXT,

            absorption TEXT,

            flow_quality TEXT

        )

        """)



    def start(self):

        self.logger.info(
            "ORDER FLOW ENGINE ONLINE"
        )



    def calculate(self, symbol, timeframe):


        candles = self.db.fetch_all("""

        SELECT
            open,
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



        buy_volume = 0

        sell_volume = 0



        for candle in candles:


            volume = candle["volume"]


            if candle["close"] > candle["open"]:

                buy_volume += volume


            elif candle["close"] < candle["open"]:

                sell_volume += volume


            else:

                buy_volume += volume * 0.5

                sell_volume += volume * 0.5



        total = buy_volume + sell_volume



        if total == 0:

            return {
                "status":"NO_VOLUME"
            }



        delta = (

            buy_volume -
            sell_volume

        ) / total



        if delta > 0.10:

            bias = "BUY_PRESSURE"


        elif delta < -0.10:

            bias = "SELL_PRESSURE"


        else:

            bias = "BALANCED"




        absorption = self.detect_absorption(
            candles,
            delta
        )



        quality = self.quality(
            abs(delta)
        )



        result = {


            "symbol":symbol,

            "timeframe":timeframe,

            "buy_volume":round(
                buy_volume,
                2
            ),

            "sell_volume":round(
                sell_volume,
                2
            ),

            "delta":round(
                delta,
                4
            ),

            "flow_bias":bias,

            "absorption":absorption,

            "flow_quality":quality

        }



        self.save(result)


        return result




    def detect_absorption(self,candles,delta):


        latest = candles[0]


        range_size = (

            latest["high"] -
            latest["low"]

        )



        if range_size == 0:

            return "FALSE"



        if abs(delta) > 0.15 and range_size < (
            latest["close"] * 0.002
        ):

            return "TRUE"



        return "FALSE"





    def quality(self,value):


        if value >= 0.25:

            return "HIGH"


        elif value >= 0.10:

            return "MEDIUM"


        return "LOW"





    def save(self,data):


        self.db.execute("""

        INSERT INTO order_flow

        (

        symbol,
        timeframe,
        timestamp,
        buy_volume,
        sell_volume,
        delta,
        flow_bias,
        absorption,
        flow_quality

        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """,

        (

        data["symbol"],
        data["timeframe"],
        int(time.time()),
        data["buy_volume"],
        data["sell_volume"],
        data["delta"],
        data["flow_bias"],
        data["absorption"],
        data["flow_quality"]

        ))
