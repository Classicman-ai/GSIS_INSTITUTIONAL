import datetime
import statistics


class GSISMarketDataOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MARKET DATA ORCHESTRATOR v3.0 ONLINE")
        print("MULTI PROVIDER CONSENSUS ENGINE ACTIVE")
        print("==============================")

        self.providers = {}
        self.provider_health = {}



    def register_provider(
        self,
        name,
        provider
    ):

        self.providers[name] = provider

        try:

            connection = provider.connect()

            self.provider_health[name] = connection


        except Exception as e:

            self.provider_health[name] = {

                "provider": name,
                "status": "FAILED",
                "error": str(e)

            }


        return self.provider_health[name]



    def health_check(self):

        results = {}

        for name in self.providers:

            try:

                results[name] = self.providers[name].health()

            except Exception as e:

                results[name] = {

                    "provider": name,
                    "status": "ERROR",
                    "error": str(e)

                }


        return {

            "status": "HEALTH CHECK COMPLETE",
            "providers": results,
            "timestamp": self.timestamp()

        }



    def healthy_providers(self):

        healthy = []

        for name, data in self.provider_health.items():

            if data.get("status") == "CONNECTED":

                healthy.append(name)


        return healthy



    def collect_quotes(
        self,
        symbol
    ):

        quotes = {}


        for name in self.healthy_providers():

            try:

                quotes[name] = self.providers[name].get_quote(
                    symbol
                )


            except Exception as e:

                quotes[name] = {

                    "status": "QUOTE ERROR",
                    "error": str(e)

                }


        return quotes




    def calculate_consensus(
        self,
        quotes
    ):


        prices = []


        for provider, data in quotes.items():

            price = data.get("price")


            if price and price > 0:

                prices.append(float(price))



        if not prices:

            return {

                "status": "NO VALID PRICES",

                "timestamp": self.timestamp()

            }



        consensus = statistics.mean(
            prices
        )


        deviation = 0


        if len(prices) > 1:

            deviation = round(

                statistics.stdev(prices),

                5

            )



        return {

            "status": "CONSENSUS PRICE COMPLETE",

            "consensus_price": round(
                consensus,
                5
            ),

            "providers_used": len(prices),

            "price_deviation": deviation,

            "confidence":

            "HIGH"

            if deviation < 0.5

            else

            "MEDIUM",

            "timestamp": self.timestamp()

        }




    def get_market_price(
        self,
        symbol
    ):


        quotes = self.collect_quotes(
            symbol
        )


        consensus = self.calculate_consensus(
            quotes
        )


        return {

            "symbol": symbol,

            "quotes": quotes,

            "consensus": consensus,

            "timestamp": self.timestamp()

        }




    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()



if __name__ == "__main__":


    from intelligence.market_data.providers.gsis_alpha_vantage_provider import (
        GSISAlphaVantageProvider
    )


    print("==============================")
    print("GSIS MARKET DATA CONSENSUS TEST")
    print("==============================")


    engine = GSISMarketDataOrchestrator()


    alpha = GSISAlphaVantageProvider()


    engine.register_provider(
        "ALPHA_VANTAGE",
        alpha
    )


    print(
        engine.health_check()
    )


    print(
        engine.get_market_price(
            "XAUUSD"
        )
    )
