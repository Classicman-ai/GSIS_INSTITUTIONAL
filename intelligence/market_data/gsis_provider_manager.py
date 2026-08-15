import os
import sys
import datetime


# ============================================================
# GSIS PACKAGE PATH CONTROL
# ============================================================

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


print("==============================")
print("GSIS PROVIDER MANAGER v3.0 ONLINE")
print("MULTI API ORCHESTRATION ENGINE ACTIVE")
print("==============================")


from intelligence.market_data.providers.gsis_alpha_vantage_provider import (
    GSISAlphaVantageProvider
)



class GSISProviderManager:


    def __init__(self):

        self.providers = {}

        self.register_default_providers()

        self.connection_status = (
            self.connect_all()
        )



    # ========================================================
    # PROVIDER REGISTRATION
    # ========================================================

    def register_default_providers(self):

        self.register_provider(

            "ALPHA_VANTAGE",

            GSISAlphaVantageProvider()

        )



    def register_provider(
        self,
        name,
        provider
    ):

        self.providers[name] = provider



    # ========================================================
    # CONNECTION MANAGEMENT
    # ========================================================

    def connect_all(self):

        results = {}


        for name, provider in self.providers.items():

            try:

                results[name] = (
                    provider.connect()
                )


            except Exception as error:

                results[name] = {

                    "provider":
                    name,

                    "status":
                    "ERROR",

                    "error":
                    str(error)

                }


        return results



    # ========================================================
    # HEALTH MONITORING
    # ========================================================

    def health_check(self):

        health = {}


        for name, provider in self.providers.items():


            try:

                if hasattr(
                    provider,
                    "health_check"
                ):

                    health[name] = (
                        provider.health_check()
                    )

                else:

                    health[name] = {

                        "status":
                        "ONLINE"

                    }


            except Exception as error:

                health[name] = {

                    "status":
                    "ERROR",

                    "error":
                    str(error)

                }


        return {

            "status":
            "HEALTH CHECK COMPLETE",

            "providers":
            health,

            "timestamp":
            self.timestamp()

        }



    # ========================================================
    # LIVE MARKET DATA ROUTER
    # ========================================================

    def get_quote(
        self,
        symbol="XAUUSD"
    ):

        quotes = {}


        for name, provider in self.providers.items():


            try:

                quotes[name] = (
                    provider.get_quote(
                        symbol
                    )
                )


            except Exception as error:

                quotes[name] = {

                    "status":
                    "ERROR",

                    "error":
                    str(error)

                }


        return {

            "symbol":
            symbol,

            "quotes":
            quotes,

            "timestamp":
            self.timestamp()

        }



    # ========================================================
    # HISTORICAL DATA ROUTER
    # ========================================================

    def get_history(
        self,
        symbol="XAUUSD",
        limit=100
    ):

        history = {}


        for name, provider in self.providers.items():


            try:

                history[name] = (
                    provider.get_candles(
                        symbol,
                        "DAILY",
                        limit
                    )
                )


            except Exception as error:

                history[name] = {

                    "status":
                    "ERROR",

                    "error":
                    str(error)

                }


        return history



    # ========================================================
    # ACTIVE PROVIDERS
    # ========================================================

    def active_providers(self):

        return {

            name:
            provider.status

            for name, provider
            in self.providers.items()

        }



    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()




if __name__ == "__main__":


    manager = GSISProviderManager()


    print("==============================")
    print("GSIS PROVIDER MANAGER TEST")
    print("==============================")


    print(
        manager.connection_status
    )


    print(
        manager.health_check()
    )


    print(
        manager.get_quote(
            "XAUUSD"
        )
    )
