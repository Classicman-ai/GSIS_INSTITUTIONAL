import datetime


class InstitutionalZoneEngine:

    def __init__(self):

        print("==============================")
        print("GSIS INSTITUTIONAL ZONE ENGINE v2.0 ONLINE")
        print("ADVANCED SUPPLY DEMAND INTELLIGENCE ACTIVE")
        print("==============================")

    def _detect_supply_demand(self, candles):

        zones = []

        for i in range(2, len(candles) - 2):

            left_high = candles[i - 1]["high"]
            center_high = candles[i]["high"]
            right_high = candles[i + 1]["high"]

            left_low = candles[i - 1]["low"]
            center_low = candles[i]["low"]
            right_low = candles[i + 1]["low"]

            # SUPPLY
            if center_high > left_high and center_high > right_high:

                departure = abs(
                    candles[i + 1]["close"] -
                    candles[i]["close"]
                )

                zones.append({

                    "type": "SUPPLY",

                    "price": center_high,

                    "index": i,

                    "fresh": True,

                    "retests": 0,

                    "departure_strength": round(departure, 2),

                    "strength": 80,

                    "status": "ACTIVE"

                })

            # DEMAND
            if center_low < left_low and center_low < right_low:

                departure = abs(
                    candles[i + 1]["close"] -
                    candles[i]["close"]
                )

                zones.append({

                    "type": "DEMAND",

                    "price": center_low,

                    "index": i,

                    "fresh": True,

                    "retests": 0,

                    "departure_strength": round(departure, 2),

                    "strength": 80,

                    "status": "ACTIVE"

                })

        return zones

    def _evaluate(self, candles, zones):

        current = candles[-1]["close"]

        for zone in zones:

            touches = 0

            for candle in candles[zone["index"] + 1:]:

                if zone["type"] == "SUPPLY":

                    if candle["high"] >= zone["price"]:

                        touches += 1

                else:

                    if candle["low"] <= zone["price"]:

                        touches += 1

            zone["retests"] = touches

            zone["fresh"] = touches == 0

            zone["distance"] = round(
                abs(current - zone["price"]),
                2
            )

            score = 100

            score -= touches * 15

            score += min(
                int(zone["departure_strength"] * 8),
                20
            )

            if score > 100:
                score = 100

            if score < 20:
                score = 20

            zone["strength"] = score

            if touches >= 3:
                zone["status"] = "WEAK"

            elif touches >= 1:
                zone["status"] = "TESTED"

            else:
                zone["status"] = "FRESH"

        return zones

    def analyze(self, candles):

        if len(candles) < 15:

            return {

                "status": "INSUFFICIENT DATA"

            }

        zones = self._detect_supply_demand(candles)

        zones = self._evaluate(candles, zones)

        nearest = None

        if zones:

            nearest = min(
                zones,
                key=lambda x: x["distance"]
            )

        demand = [
            z for z in zones
            if z["type"] == "DEMAND"
        ]

        supply = [
            z for z in zones
            if z["type"] == "SUPPLY"
        ]

        result = {

            "status": "ZONE ANALYSIS COMPLETE",

            "total_zones": len(zones),

            "demand_zones": len(demand),

            "supply_zones": len(supply),

            "nearest_zone": nearest,

            "zones": zones,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }

        print("==============================")
        print("GSIS INSTITUTIONAL ZONE RESULT")
        print("==============================")
        print(result)

        return result


if __name__ == "__main__":

    candles = []

    price = 2385.0

    for i in range(30):

        candles.append({

            "open": price,

            "high": price + 0.8,

            "low": price - 0.7,

            "close": price + 0.2

        })

        if i % 6 == 0:

            price += 1.6

        elif i % 9 == 0:

            price -= 1.2

        else:

            price += 0.25

    engine = InstitutionalZoneEngine()

    engine.analyze(candles)
