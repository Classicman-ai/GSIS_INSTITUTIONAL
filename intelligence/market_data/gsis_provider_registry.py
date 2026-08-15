import datetime


class GSISProviderRegistry:

    def __init__(self):

        self.providers = {}

        print("==============================")
        print("GSIS PROVIDER REGISTRY v1.0 ONLINE")
        print("CAPABILITY MANAGEMENT ENGINE ACTIVE")
        print("==============================")


    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()


    def register_provider(
        self,
        name,
        provider,
        capabilities
    ):

        self.providers[name] = {

            "instance": provider,

            "capabilities": capabilities,

            "registered": self.timestamp()

        }


        return {

            "status": "PROVIDER REGISTERED",

            "provider": name,

            "capabilities": capabilities,

            "timestamp": self.timestamp()

        }


    def unregister_provider(self, name):

        if name in self.providers:

            del self.providers[name]

            return {

                "status": "PROVIDER REMOVED",

                "provider": name

            }


        return {

            "status": "PROVIDER NOT FOUND",

            "provider": name

        }


    def get_provider(self, name):

        provider = self.providers.get(name)


        if provider:

            return provider["instance"]


        return None



    def get_by_capability(self, capability):

        results = []


        for name, data in self.providers.items():

            if data["capabilities"].get(
                capability,
                False
            ):

                results.append(name)


        return results



    def list_providers(self):

        output = {}


        for name, data in self.providers.items():

            output[name] = {

                "capabilities":
                data["capabilities"],

                "registered":
                data["registered"]

            }


        return output



    def health_check(self):

        result = {}


        for name, data in self.providers.items():

            provider = data["instance"]


            try:

                result[name] = provider.health()


            except Exception as e:

                result[name] = {

                    "status": "ERROR",

                    "error": str(e)

                }


        return {

            "status":
            "REGISTRY HEALTH COMPLETE",

            "providers":
            result,

            "timestamp":
            self.timestamp()

        }



if __name__ == "__main__":


    print("==============================")
    print("GSIS PROVIDER REGISTRY TEST")
    print("==============================")


    registry = GSISProviderRegistry()


    print(
        registry.register_provider(
            "TEST_PROVIDER",
            object(),
            {
                "price": True,
                "history": False,
                "news": True,
                "fundamentals": False,
                "sentiment": False
            }
        )
    )


    print(registry.list_providers())


    print(
        registry.get_by_capability(
            "news"
        )
    )
