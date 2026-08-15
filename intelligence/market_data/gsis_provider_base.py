import datetime


class GSISProviderBase:

    def __init__(self, name):

        self.name = name
        self.status = "INITIALIZED"
        self.last_check = None


    def connect(self):

        raise NotImplementedError(
            "Provider connect() not implemented"
        )


    def health(self):

        return {

            "provider": self.name,

            "status": self.status,

            "last_check": self.last_check

        }


    def get_quote(self, symbol):

        raise NotImplementedError(
            "Provider quote method not implemented"
        )


    def get_candles(
        self,
        symbol,
        timeframe,
        limit
    ):

        raise NotImplementedError(
            "Provider candle method not implemented"
        )


    def download_history(
        self,
        symbol,
        timeframe,
        start,
        end
    ):

        raise NotImplementedError(
            "Provider history method not implemented"
        )


    def timestamp(self):

        return datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
