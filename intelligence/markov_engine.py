"""
=========================================================
GSIS INSTITUTIONAL

MARKOV MARKET STATE PROBABILITY ENGINE
Version: 1.0

Probabilistic Market Regime Transition Model

States:

ACCUMULATION
MARKUP
DISTRIBUTION
MARKDOWN
RANGE

=========================================================
"""


class MarkovEngine:


    def __init__(self):

        self.name = "Markov Market State Engine"

        self.status = "CREATED"


        self.states = [

            "ACCUMULATION",

            "MARKUP",

            "DISTRIBUTION",

            "MARKDOWN",

            "RANGE"

        ]


        self.transition_matrix = {


            "ACCUMULATION": {

                "MARKUP": 0.65,

                "RANGE": 0.20,

                "DISTRIBUTION": 0.10,

                "MARKDOWN": 0.05

            },


            "MARKUP": {

                "DISTRIBUTION": 0.60,

                "MARKUP": 0.25,

                "RANGE": 0.10,

                "MARKDOWN": 0.05

            },


            "DISTRIBUTION": {

                "MARKDOWN": 0.65,

                "RANGE": 0.20,

                "MARKUP": 0.10,

                "ACCUMULATION": 0.05

            },


            "MARKDOWN": {

                "ACCUMULATION": 0.55,

                "RANGE": 0.25,

                "MARKDOWN": 0.15,

                "MARKUP": 0.05

            },


            "RANGE": {

                "ACCUMULATION": 0.35,

                "DISTRIBUTION": 0.25,

                "MARKUP": 0.20,

                "MARKDOWN": 0.20

            }

        }



    def initialize(self):

        self.status = "ONLINE"


        print("==============================")

        print(
            "MARKOV PROBABILITY ENGINE ONLINE"
        )

        print("==============================")



    def predict_transition(
            self,
            current_state):


        if current_state not in self.transition_matrix:

            return None



        probabilities = self.transition_matrix[
            current_state
        ]



        next_state = max(

            probabilities,

            key=probabilities.get

        )



        return {


            "current_state":

            current_state,


            "probabilities":

            probabilities,


            "most_likely_transition":

            next_state,


            "confidence":

            probabilities[next_state]

        }



    def analyze(
            self,
            regime):


        if not regime:

            return None



        current_state = regime.get(

            "regime",

            "RANGE"

        )


        result = self.predict_transition(

            current_state

        )


        return result



    def shutdown(self):

        self.status = "OFFLINE"


        print(
            "MARKOV ENGINE STOPPED"
        )
