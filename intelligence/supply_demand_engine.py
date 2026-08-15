"""
=========================================================
GSIS INSTITUTIONAL

SUPPLY DEMAND INTELLIGENCE ENGINE

Version 1.0

Institutional Zone Detection

=========================================================
"""


from datetime import datetime



class SupplyDemandEngine:


    def __init__(self):

        self.name = "Supply Demand Engine"

        self.status = "CREATED"

        self.zones = []




    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("SUPPLY DEMAND ENGINE ONLINE")
        print("==============================")





    def analyze(self, candles):


        if not candles:

            return None



        latest = candles[-1]


        zone = {


            "timestamp":
            str(datetime.utcnow()),


            "symbol":
            latest.get("symbol"),


            "price":
            latest.get("close"),


            "zone_type":
            self.detect_zone(candles),


            "strength":
            self.calculate_strength(candles),


            "status":
            "ACTIVE"

        }


        self.zones.append(zone)


        return zone





    def detect_zone(self, candles):


        if len(candles) < 3:

            return "UNKNOWN"


        previous = candles[-2]

        current = candles[-1]



        if current["close"] > previous["close"]:

            return "DEMAND"


        elif current["close"] < previous["close"]:

            return "SUPPLY"


        return "NEUTRAL"





    def calculate_strength(self, candles):


        movement = abs(
            candles[-1]["close"]
            -
            candles[-2]["close"]
        )


        if movement > 0:

            return "STRONG"


        return "WEAK"





    def latest_zone(self):


        if self.zones:

            return self.zones[-1]


        return None
