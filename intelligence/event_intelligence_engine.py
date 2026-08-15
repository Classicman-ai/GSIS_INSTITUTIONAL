"""
=========================================================
GSIS INSTITUTIONAL

EVENT INTELLIGENCE ENGINE

Version 1.0

Institutional Market Event Risk Controller

=========================================================
"""


from datetime import datetime



class EventIntelligenceEngine:


    def __init__(self):

        self.name = "Event Intelligence Engine"

        self.status = "CREATED"

        self.events = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("EVENT INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def analyze(self, event):


        impact = self.classify_event(
            event
        )


        result = {


            "timestamp":

            str(datetime.utcnow()),


            "event":

            event,


            "impact":

            impact,


            "trading_mode":

            self.trading_mode(
                impact
            ),


            "execution":

            self.execution_permission(
                impact
            )

        }



        self.events.append(result)


        return result






    def classify_event(self, event):


        high = [

            "CPI",

            "NFP",

            "FOMC",

            "INTEREST RATE",

            "FED SPEECH"

        ]



        medium = [

            "GDP",

            "PMI",

            "EMPLOYMENT"

        ]



        name = event.upper()



        for item in high:

            if item in name:

                return "HIGH IMPACT"




        for item in medium:

            if item in name:

                return "MEDIUM IMPACT"



        return "LOW IMPACT"






    def trading_mode(self, impact):


        if impact == "HIGH IMPACT":

            return "REDUCED RISK"



        elif impact == "MEDIUM IMPACT":

            return "CAUTION"



        return "NORMAL"






    def execution_permission(self, impact):


        if impact == "HIGH IMPACT":

            return "RESTRICTED"



        return "APPROVED"






    def latest(self):


        if self.events:

            return self.events[-1]


        return None
