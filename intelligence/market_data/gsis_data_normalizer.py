import datetime


class GSISDataNormalizer:


    def __init__(self):

        print("==============================")
        print("GSIS DATA NORMALIZER v1.0 ONLINE")
        print("MULTI PROVIDER DATA STANDARDIZATION ACTIVE")
        print("==============================")



    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()



    def normalize_quote(
        self,
        provider,
        symbol,
        data
    ):

        price = None


        # Direct numeric response

        if isinstance(
            data,
            (int, float)
        ):

            price = data



        # Dictionary response

        elif isinstance(
            data,
            dict
        ):

            price = (

                data.get("price")

                or

                data.get("close")

                or

                data.get("last")

            )



        if price is None:


            return {

                "provider": provider,

                "symbol": symbol,

                "status": "INVALID",

                "price": None,

                "timestamp": self.timestamp()

            }



        return {

            "provider": provider,

            "symbol": symbol,

            "price": float(price),

            "status": "VALID",

            "quality": "NORMALIZED",

            "timestamp": self.timestamp()

        }



    def normalize_quotes(
        self,
        symbol,
        quotes
    ):


        normalized = []


        for provider, data in quotes.items():


            normalized.append(

                self.normalize_quote(

                    provider,

                    symbol,

                    data

                )

            )



        return normalized




if __name__ == "__main__":


    print("==============================")
    print("GSIS DATA NORMALIZER TEST")
    print("==============================")


    normalizer = GSISDataNormalizer()



    test = {

        "ALPHA_VANTAGE": {

            "price": 4051.28

        },


        "TWELVE_DATA": 4050.38

    }



    print(

        normalizer.normalize_quotes(

            "XAUUSD",

            test

        )

    )
