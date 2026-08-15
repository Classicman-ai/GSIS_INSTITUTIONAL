"""
=========================================================
GSIS INSTITUTIONAL
CANDLE ENGINE
Version: 2.1

Managed Module Architecture
Timestamp Hardened
=========================================================
"""

from datetime import datetime



class CandleEngine:


    def __init__(self):

        self.name = "Candle Engine"

        self.timeframes = {

            "M1": 60,

            "M5": 300,

            "M15": 900,

            "M30": 1800,

            "H1": 3600,

            "H4": 14400,

            "D1": 86400

        }

        self.candles = {}

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("GSIS CANDLE ENGINE ONLINE")
        print("==============================")



    def convert_timestamp(self, timestamp):


        if isinstance(timestamp, datetime):

            return int(timestamp.timestamp())



        if isinstance(timestamp, str):

            try:

                dt = datetime.fromisoformat(
                    timestamp
                )

                return int(
                    dt.timestamp()
                )

            except Exception:

                return int(
                    datetime.utcnow().timestamp()
                )



        return int(
            datetime.utcnow().timestamp()
        )



    def update(self, market_data):


        if market_data is None:

            return None



        price = market_data["price"]

        timestamp = self.convert_timestamp(
            market_data["time"]
        )



        generated = {}



        for timeframe, seconds in self.timeframes.items():


            candle = self.candles.get(
                timeframe
            )


            candle_start = (

                timestamp //

                seconds

            ) * seconds



            if candle is None:


                candle = {

                    "timeframe": timeframe,

                    "timestamp": candle_start,

                    "open": price,

                    "high": price,

                    "low": price,

                    "close": price

                }



            elif candle["timestamp"] == candle_start:


                candle["high"] = max(

                    candle["high"],

                    price

                )


                candle["low"] = min(

                    candle["low"],

                    price

                )


                candle["close"] = price



            else:


                generated[timeframe] = candle



                candle = {


                    "timeframe": timeframe,

                    "timestamp": candle_start,

                    "open": price,

                    "high": price,

                    "low": price,

                    "close": price

                }



            self.candles[timeframe] = candle



        return generated



    def shutdown(self):

        self.status = "OFFLINE"

        print(
            "CANDLE ENGINE STOPPED"
        )
