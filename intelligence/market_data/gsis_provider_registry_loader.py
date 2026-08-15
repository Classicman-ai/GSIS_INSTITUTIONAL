from intelligence.market_data.gsis_provider_registry import GSISProviderRegistry

from intelligence.market_data.providers.gsis_alpha_vantage_provider import (
    GSISAlphaVantageProvider
)

from intelligence.market_data.providers.gsis_twelve_data_provider import (
    GSISTwelveDataProvider
)

from intelligence.market_data.providers.gsis_finnhub_provider import (
    GSISFinnhubProvider
)

from intelligence.market_data.providers.gsis_fmp_provider import (
    GSISFMPProvider
)

from intelligence.market_data.providers.gsis_news_provider import (
    GSISNewsProvider
)


class GSISProviderRegistryLoader:


    def __init__(self):

        self.registry = GSISProviderRegistry()



    def load(self):


        alpha = GSISAlphaVantageProvider()

        twelve = GSISTwelveDataProvider()

        finnhub = GSISFinnhubProvider()

        fmp = GSISFMPProvider()

        news = GSISNewsProvider()



        self.registry.register_provider(

            "ALPHA_VANTAGE",

            alpha,

            {
                "price": True,
                "history": True,
                "news": False,
                "fundamentals": False,
                "sentiment": False
            }

        )


        self.registry.register_provider(

            "TWELVE_DATA",

            twelve,

            {
                "price": True,
                "history": False,
                "news": False,
                "fundamentals": False,
                "sentiment": False
            }

        )


        self.registry.register_provider(

            "FINNHUB",

            finnhub,

            {
                "price": False,
                "history": False,
                "news": True,
                "fundamentals": False,
                "sentiment": True
            }

        )


        self.registry.register_provider(

            "FMP",

            fmp,

            {
                "price": False,
                "history": False,
                "news": False,
                "fundamentals": True,
                "sentiment": False
            }

        )


        self.registry.register_provider(

            "NEWS_API",

            news,

            {
                "price": False,
                "history": False,
                "news": True,
                "fundamentals": False,
                "sentiment": False
            }

        )


        return self.registry



if __name__ == "__main__":


    print("==============================")
    print("GSIS REGISTRY LOADER TEST")
    print("==============================")


    loader = GSISProviderRegistryLoader()

    registry = loader.load()


    print(registry.list_providers())


    print(
        registry.get_by_capability(
            "price"
        )
    )


    print(
        registry.get_by_capability(
            "news"
        )
    )
