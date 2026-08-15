"""
=========================================================
GSIS INSTITUTIONAL

MARKET REGIME INTELLIGENCE ENGINE

Version 2.0

Adaptive Market Environment Classification

=========================================================
"""


from datetime import datetime



class MarketRegimeIntelligenceEngine:



    def __init__(self):

        self.name = "Market Regime Intelligence Engine"

        self.status = "CREATED"

        self.history = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("MARKET REGIME INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(self, candles):


        if len(candles) < 20:

            return None



        closes = [
            c["close"]
            for c in candles[-20:]
        ]



        trend = self.detect_trend(
            closes
        )


        volatility = self.detect_volatility(
            closes
        )


        regime = self.classify(
            trend,
            volatility
        )



        result = {


            "timestamp":

            str(datetime.utcnow()),


            "trend":

            trend,


            "volatility":

            volatility,


            "regime":

            regime,


            "trading_mode":

            self.trading_mode(regime)

        }



        self.history.append(result)


        return result






    def detect_trend(self, closes):


        first = closes[0]

        last = closes[-1]



        change = (
            last - first
        ) / first * 100



        if change > 1:

            return "BULLISH"



        elif change < -1:

            return "BEARISH"



        return "NEUTRAL"






    def detect_volatility(self, closes):


        average = sum(closes) / len(closes)


        deviations = []


        for price in closes:

            deviations.append(
                abs(price - average)
            )



        volatility = (
            sum(deviations)
            /
            len(deviations)
            /
            average
        ) * 100



        if volatility > 2:

            return "HIGH"



        elif volatility < 0.5:

            return "LOW"



        return "NORMAL"






    def classify(
            self,
            trend,
            volatility):


        if (
            trend == "BULLISH"
            and
            volatility != "HIGH"
        ):

            return "TRENDING BULLISH"



        if (
            trend == "BEARISH"
            and
            volatility != "HIGH"
        ):

            return "TRENDING BEARISH"



        if volatility == "HIGH":

            return "HIGH VOLATILITY"



        return "RANGE MARKET"






    def trading_mode(
            self,
            regime):


        if regime == "TRENDING BULLISH":

            return "BUY ONLY"



        if regime == "TRENDING BEARISH":

            return "SELL ONLY"



        if regime == "RANGE MARKET":

            return "MEAN REVERSION"



        return "REDUCED RISK"






    def latest(self):

        if self.history:

            return self.history[-1]


        return None
