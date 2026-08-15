"""
=========================================================
GSIS INSTITUTIONAL

PORTFOLIO INTELLIGENCE &
CAPITAL ALLOCATION ENGINE

Version 1.0

Portfolio Management Layer

=========================================================
"""


from datetime import datetime
import uuid



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





    def register_asset(
            self,
            symbol):


        asset = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "time":

            str(datetime.utcnow())

        }



        self.assets.append(asset)


        return asset






    def allocate_capital(
            self,
            asset,
            percentage):


        allocation = {


            "asset":

            asset,


            "allocation":

            percentage,


            "time":

            str(datetime.utcnow())

        }



        self.allocations.append(allocation)


        return allocation






    def record_risk(
            self,
            asset,
            risk_level):


        data = {


            "asset":

            asset,


            "risk":

            risk_level,


            "time":

            str(datetime.utcnow())

        }



        self.risk_records.append(data)


        return data






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
