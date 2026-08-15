import datetime

from intelligence.market_data.gsis_provider_registry_loader import (
    GSISProviderRegistryLoader
)

from intelligence.market_data.gsis_data_normalizer import (
    GSISDataNormalizer
)


class GSISMarketDataOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MARKET DATA ORCHESTRATOR v6.0 ONLINE")
        print("NORMALIZED MULTI PROVIDER CONSENSUS ENGINE ACTIVE")
        print("==============================")


        self.loader = GSISProviderRegistryLoader()

        self.registry = self.loader.load()

        self.normalizer = GSISDataNormalizer()



    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()



    def health_check(self):

        return self.registry.health_check()



    def get_price_providers(self):

        return self.registry.get_by_capability(
            "price"
        )



    def collect_quotes(
        self,
        symbol="XAUUSD"
    ):


        quotes = {}


        providers = self.get_price_providers()


        for name in providers:


            provider = self.registry.get_provider(
                name
            )


            try:


                result = provider.get_quote(
                    symbol
                )


                quotes[name] = result



            except Exception as error:


                quotes[name] = {

                    "error": str(error)

                }



        return quotes




    def normalized_market_data(
        self,
        symbol="XAUUSD"
    ):


        raw_quotes = self.collect_quotes(
            symbol
        )


        return self.normalizer.normalize_quotes(
            symbol,
            raw_quotes
        )



    def consensus(
        self,
        normalized
    ):


        prices = []


        for item in normalized:


            if item.get("status") == "VALID":


                prices.append(
                    item["price"]
                )



        if not prices:


            return {

                "status":
                "NO VALID MARKET DATA",

                "timestamp":
                self.timestamp()

            }



        consensus_price = sum(prices) / len(prices)


        spread = max(prices) - min(prices)



        confidence = "HIGH"


        if spread > 5:

            confidence = "WARNING"



        return {


            "status":
            "CONSENSUS COMPLETE",


            "consensus_price":
            round(
                consensus_price,
                5
            ),


            "highest":
            max(prices),


            "lowest":
            min(prices),


            "spread":
            round(
                spread,
                5
            ),


            "providers_used":
            len(prices),


            "confidence":
            confidence,


            "timestamp":
            self.timestamp()

        }




if __name__ == "__main__":


    print("==============================")
    print("GSIS MARKET DATA CONSENSUS TEST")
    print("==============================")


    engine = GSISMarketDataOrchestrator()


    print(
        engine.health_check()
    )


    data = engine.normalized_market_data(
        "XAUUSD"
    )


    print(
        data
    )


    print(
        engine.consensus(
            data
        )
    )
