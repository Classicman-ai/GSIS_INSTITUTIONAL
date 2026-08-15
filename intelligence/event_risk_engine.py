"""
=========================================================
GSIS INSTITUTIONAL

EVENT RISK INTELLIGENCE ENGINE
Version: 1.0

Institutional Macro Risk Layer

Functions:
- Event monitoring
- Volatility risk
- Trading permission control

=========================================================
"""


class EventRiskEngine:


    def __init__(self):

        self.name = "Event Risk Intelligence Engine"

        self.status = "CREATED"


        self.high_risk_events = [

            "CPI",

            "NFP",

            "FOMC",

            "RATE_DECISION"

        ]



    def initialize(self):

        self.status = "ONLINE"


        print("==============================")

        print(
            "EVENT RISK INTELLIGENCE ENGINE ONLINE"
        )

        print("==============================")



    def analyze_event(
            self,
            event):


        if not event:


            return {


                "risk":

                "LOW",


                "permission":

                "ALLOWED"

            }



        event_name = event.get(

            "name",

            ""

        )



        if event_name in self.high_risk_events:


            return {


                "event":

                event_name,


                "risk":

                "HIGH",


                "permission":

                "BLOCK"

            }



        return {


            "event":

            event_name,


            "risk":

            "MEDIUM",


            "permission":

            "CAUTION"

        }



    def volatility_check(
            self,
            volatility,
            average):


        if average == 0:

            return "UNKNOWN"



        ratio = volatility / average



        if ratio >= 3:


            return "VOLATILITY SHOCK"



        elif ratio >= 2:


            return "ELEVATED"



        else:


            return "NORMAL"



    def trading_permission(
            self,
            event_risk):


        if event_risk == "HIGH":


            return "BLOCK"



        return "ALLOW"



    def shutdown(self):

        self.status = "OFFLINE"


        print(
            "EVENT RISK ENGINE STOPPED"
        )
