"""
=========================================================
GSIS INSTITUTIONAL

DASHBOARD DATA ENGINE

Version 1.0

Institutional Visualization Data Layer

=========================================================
"""


from datetime import datetime



class DashboardDataEngine:


    def __init__(self):

        self.name = "Dashboard Data Engine"

        self.status = "CREATED"

        self.data = {}





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DASHBOARD DATA ENGINE ONLINE")
        print("==============================")





    def update_market_state(
            self,
            state):


        self.data["market"] = state





    def update_signal(
            self,
            signal):


        self.data["signal"] = signal





    def update_risk(
            self,
            risk):


        self.data["risk"] = risk





    def update_system(
            self,
            system):


        self.data["system"] = system





    def generate_dashboard(self):


        return {


            "timestamp":

            str(datetime.utcnow()),


            "status":

            self.status,


            "dashboard":

            self.data

        }





    def get_section(
            self,
            section):


        return self.data.get(
            section,
            {}
        )
