import datetime


class GSISMarketDataOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MARKET DATA ORCHESTRATOR v2.0 ONLINE")
        print("MULTI PROVIDER REGISTRY + HEALTH CONTROL ACTIVE")
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

                "status": "CONNECTION FAILED",

                "error": str(e),

                "timestamp": self.timestamp()

            }



        return {

            "status":
            "PROVIDER REGISTERED",

            "provider":
            name,

            "health":
            self.provider_health[name],

            "timestamp":
            self.timestamp()

        }




    def check_provider_health(
        self,
        name
    ):


        if name not in self.providers:

            return {

                "status":
                "PROVIDER NOT FOUND",

                "provider":
                name

            }



        try:

            health = self.providers[name].health()


            self.provider_health[name] = health


            return health



        except Exception as e:


            result = {

                "provider":
                name,

                "status":
                "HEALTH ERROR",

                "error":
                str(e),

                "timestamp":
                self.timestamp()

            }


            self.provider_health[name] = result


            return result





    def health_check(self):


        results = {}


        for name in self.providers:


            results[name] = self.check_provider_health(
                name
            )


        return {

            "status":
            "MARKET DATA HEALTH COMPLETE",

            "providers":
            results,

            "timestamp":
            self.timestamp()

        }





    def healthy_providers(self):


        healthy = []


        for name, health in self.provider_health.items():


            if health.get("status") == "CONNECTED":

                healthy.append(name)



        return healthy





    def get_provider(
        self,
        name
    ):


        return self.providers.get(
            name
        )





    def best_provider(self):


        providers = self.healthy_providers()


        if not providers:

            return None



        return self.providers[

            providers[0]

        ]





    def provider_count(self):


        return len(

            self.providers

        )





    def get_quotes(
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

                    "status":
                    "QUOTE ERROR",

                    "error":
                    str(e)

                }



        return {

            "symbol":
            symbol,

            "quotes":
            quotes,

            "timestamp":
            self.timestamp()

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
    print("GSIS MARKET DATA ORCHESTRATOR TEST")
    print("==============================")


    orchestrator = GSISMarketDataOrchestrator()


    alpha = GSISAlphaVantageProvider()


    print(

        orchestrator.register_provider(

            "ALPHA_VANTAGE",

            alpha

        )

    )


    print(

        orchestrator.health_check()

    )


    print(

        {

            "provider_count":
            orchestrator.provider_count(),

            "healthy":
            orchestrator.healthy_providers()

        }

    )


    print(

        orchestrator.get_quotes(
            "XAUUSD"
        )

    )
