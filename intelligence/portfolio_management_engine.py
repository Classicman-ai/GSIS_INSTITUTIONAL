"""
=========================================================
GSIS INSTITUTIONAL

PORTFOLIO & EXPOSURE MANAGEMENT ENGINE

Version 1.0

Institutional Capital Control Layer

=========================================================
"""


from datetime import datetime



class PortfolioManagementEngine:


    def __init__(self):

        self.name = "Portfolio Management Engine"

        self.status = "CREATED"

        self.positions = []

        self.max_exposure = 5.0





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("PORTFOLIO MANAGEMENT ENGINE ONLINE")
        print("==============================")





    def add_position(
            self,
            position):


        self.positions.append(
            position
        )


        return self.exposure_report()






    def remove_position(
            self,
            symbol):


        self.positions = [

            p for p in self.positions

            if p.get("symbol") != symbol

        ]


        return self.exposure_report()






    def total_exposure(self):


        total = 0


        for position in self.positions:


            total += position.get(
                "risk",
                0
            )


        return total






    def check_permission(self):


        exposure = self.total_exposure()


        if exposure >= self.max_exposure:


            return {


                "permission":

                "BLOCKED",


                "reason":

                "MAX EXPOSURE REACHED"

            }




        return {


            "permission":

            "APPROVED",


            "remaining":

            self.max_exposure - exposure

        }






    def exposure_report(self):


        return {


            "timestamp":

            str(datetime.utcnow()),


            "positions":

            len(self.positions),


            "total_exposure":

            self.total_exposure(),


            "permission":

            self.check_permission()

        }






    def correlation_check(
            self,
            new_asset):


        correlated = []


        for position in self.positions:


            if position.get("asset_class") == new_asset.get("asset_class"):


                correlated.append(
                    position.get("symbol")
                )



        return {


            "correlated_positions":

            correlated,


            "risk":

            "HIGH"

            if len(correlated) > 2

            else

            "NORMAL"

        }
