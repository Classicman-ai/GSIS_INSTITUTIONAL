"""
=========================================================
GSIS INSTITUTIONAL

MULTI-VENUE EXECUTION INTELLIGENCE ENGINE (MVEI)

Version: 1.0

Functions:
- Compare execution venues
- Rank liquidity sources
- Select optimal venue

=========================================================
"""


from datetime import datetime



class MultiVenueEngine:


    def __init__(self):


        self.name = "Multi-Venue Execution Intelligence Engine"

        self.status = "CREATED"

        self.venues = []



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "MULTI-VENUE EXECUTION ENGINE ONLINE"
        )

        print("==============================")



    def add_venue(
            self,
            name,
            latency,
            fill_rate,
            liquidity):


        venue = {


            "name":
            name,


            "latency":
            latency,


            "fill_rate":
            fill_rate,


            "liquidity":
            liquidity

        }


        self.venues.append(
            venue
        )


        return venue



    def evaluate(self):


        ranking = []



        for venue in self.venues:


            score = self.calculate_score(
                venue
            )


            ranking.append({

                "venue":
                venue["name"],

                "score":
                score

            })



        ranking.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return {


            "timestamp":
            str(datetime.utcnow()),


            "ranking":
            ranking,


            "selected":
            ranking[0]
            if ranking
            else None

        }



    def calculate_score(
            self,
            venue):


        score = venue["fill_rate"]



        if venue["latency"] < 100:


            score += 5



        elif venue["latency"] > 500:


            score -= 10



        if venue["liquidity"] == "HIGH":


            score += 5



        elif venue["liquidity"] == "LOW":


            score -= 15



        return round(
            score,
            2
        )
