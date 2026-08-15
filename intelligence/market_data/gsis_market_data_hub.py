import os
import sys
import sqlite3
import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )


from intelligence.market_data.gsis_provider_manager import (
    GSISProviderManager
)


print("==============================")
print("GSIS MARKET DATA HUB v1.0 ONLINE")
print("LIVE + HISTORICAL DATA PIPELINE ACTIVE")
print("==============================")


DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "gsis_market_database.sqlite"
)



class GSISMarketDataHub:


    def __init__(self):

        self.manager = GSISProviderManager()

        self.connection = sqlite3.connect(
            DATABASE
        )

        self.create_tables()



    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS live_market_data
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            provider TEXT,
            timestamp TEXT
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historical_candles
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            provider TEXT
            )
            """
        )


        self.connection.commit()



    def update_live_price(
        self,
        symbol="XAUUSD"
    ):


        data = self.manager.get_quote(
            symbol
        )


        cursor = self.connection.cursor()


        for provider, quote in data["providers"].items():

            if quote.get("price"):


                cursor.execute(

                    """
                    INSERT INTO live_market_data
                    (
                    symbol,
                    price,
                    provider,
                    timestamp
                    )

                    VALUES (?,?,?,?)

                    """,

                    (

                    symbol,

                    quote["price"],

                    provider,

                    quote["timestamp"]

                    )

                )


        self.connection.commit()


        return data



    def download_history(
        self,
        symbol="XAUUSD",
        limit=100
    ):


        data = self.manager.get_history(
            symbol,
            limit
        )


        cursor = self.connection.cursor()


        for provider, result in data.items():

            for candle in result.get(
                "candles",
                []
            ):


                cursor.execute(

                    """
                    INSERT INTO historical_candles
                    (
                    symbol,
                    date,
                    open,
                    high,
                    low,
                    close,
                    provider
                    )

                    VALUES (?,?,?,?,?,?,?)

                    """,

                    (

                    symbol,

                    candle["date"],

                    candle["open"],

                    candle["high"],

                    candle["low"],

                    candle["close"],

                    provider

                    )

                )


        self.connection.commit()


        return {

            "status":
            "HISTORY IMPORT COMPLETE",

            "records":
            len(
                data
            )

        }



    def status(self):

        return {

            "database":
            DATABASE,

            "timestamp":
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()

        }



if __name__ == "__main__":


    hub = GSISMarketDataHub()


    print("==============================")
    print("GSIS MARKET DATA HUB TEST")
    print("==============================")


    print(
        hub.update_live_price(
            "XAUUSD"
        )
    )


    print(
        hub.download_history(
            "XAUUSD",
            50
        )
    )


    print(
        hub.status()
    )
