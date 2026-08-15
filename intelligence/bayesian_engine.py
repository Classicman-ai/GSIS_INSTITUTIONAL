"""
=========================================================
GSIS INSTITUTIONAL
BAYESIAN EVIDENCE ENGINE
Version: 2.0

Evidence-Based Probability Calculation
=========================================================
"""


class BayesianEngine:


    def __init__(self):

        self.name = "Bayesian Evidence Engine"

        self.status = "CREATED"



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("BAYESIAN EVIDENCE ENGINE ONLINE")
        print("==============================")



    def calculate_probability(
            self,
            historical_matches,
            successful_matches,
            total_events):


        if total_events == 0:


            return {

                "probability": 50,

                "confidence": "LOW"

            }



        prior = (

            successful_matches /

            total_events

        ) * 100



        # Bayesian confidence adjustment

        if total_events >= 100:


            confidence = "HIGH"


        elif total_events >= 30:


            confidence = "MEDIUM"


        else:


            confidence = "LOW"



        return {


            "probability":

            round(prior, 2),


            "historical_matches":

            historical_matches,


            "sample_size":

            total_events,


            "confidence":

            confidence

        }



    def update_from_pattern(
            self,
            pattern_data):


        return self.calculate_probability(

            pattern_data.get(
                "matches",
                0
            ),


            pattern_data.get(
                "successful",
                0
            ),


            pattern_data.get(
                "total",
                0
            )

        )
