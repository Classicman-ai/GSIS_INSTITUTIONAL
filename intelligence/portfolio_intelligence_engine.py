"""
=========================================================
GSIS INSTITUTIONAL

PORTFOLIO INTELLIGENCE ENGINE

Version 1.0

Institutional Capital Management Layer

=========================================================
"""


from datetime import datetime



class PortfolioIntelligenceEngine:


    def __init__(self):

        self.name = "Portfolio Intelligence Engine"

        self.status = "CREATED"

        self.assets = []

        self.allocations = []

        self.risk_records = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("PORTFOLIO INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def add_asset(
            self,
            symbol,
            exposure):


        asset = {


            "symbol":

            symbol,


            "exposure":

            exposure,


            "time":

            str(datetime.utcnow())

        }



        self.assets.append(asset)


        return asset






    def allocate_capital(
            self,
            strategy,
            percentage):


        allocation = {


            "strategy":

            strategy,


            "allocation":

            percentage,


            "time":

            str(datetime.utcnow())

        }



        self.allocations.append(allocation)


        return allocation






    def record_risk(
            self,
            category,
            value):


        risk = {


            "category":

            category,


            "value":

            value,


            "time":

            str(datetime.utcnow())

        }



        self.risk_records.append(risk)


        return risk






    def portfolio_report(self):


        return {


            "status":

            self.status,


            "assets":

            len(self.assets),


            "allocations":

            len(self.allocations),


            "risk_records":

            len(self.risk_records)

        }
