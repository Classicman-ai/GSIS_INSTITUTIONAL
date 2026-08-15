"""
=========================================================
GSIS INSTITUTIONAL

SIMULATION & BACKTESTING INTELLIGENCE ENGINE

Version 1.0

Historical Research Laboratory Layer

=========================================================
"""


from datetime import datetime



class BacktestingEngine:


    def __init__(self):

        self.name = "Backtesting Engine"

        self.status = "CREATED"

        self.sessions = []

        self.results = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("BACKTESTING ENGINE ONLINE")
        print("==============================")





    def create_session(
            self,
            asset,
            timeframe,
            start,
            end):


        session = {


            "asset":

            asset,


            "timeframe":

            timeframe,


            "start":

            start,


            "end":

            end,


            "created":

            str(datetime.utcnow()),


            "status":

            "CREATED"

        }



        self.sessions.append(session)


        return session






    def run_test(
            self,
            session,
            strategy):


        result = {


            "strategy":

            strategy,


            "session":

            session,


            "trades":

            0,


            "wins":

            0,


            "losses":

            0,


            "profit":

            0,


            "drawdown":

            0,


            "status":

            "COMPLETED"

        }



        self.results.append(result)


        return result






    def evaluate(
            self,
            result):


        trades = result["trades"]


        if trades == 0:


            return {


                "rating":

                "INSUFFICIENT DATA"

            }



        win_rate = (

            result["wins"]

            /

            trades

        ) * 100



        return {


            "win_rate":

            win_rate,


            "drawdown":

            result["drawdown"],


            "profit":

            result["profit"]

        }






    def report(self):


        return {


            "engine":

            self.status,


            "sessions":

            len(self.sessions),


            "tests":

            len(self.results)

        }
