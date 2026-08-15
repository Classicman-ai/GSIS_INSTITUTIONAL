"""
=========================================================
GSIS INSTITUTIONAL

MARKET REPLAY CONTROLLER

Version 1.0

Institutional Research Simulation Controller

=========================================================
"""


from datetime import datetime
import uuid
import time



class MarketReplayController:



    def __init__(self):

        self.name = "Market Replay Controller"

        self.status = "CREATED"

        self.sessions = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("MARKET REPLAY CONTROLLER ONLINE")
        print("==============================")





    def create_session(
            self,
            symbol,
            candles):


        session = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "candles":

            candles,


            "processed":

            0,


            "signals":

            [],


            "start_time":

            str(datetime.utcnow())

        }


        self.sessions.append(session)


        return session






    def replay(
            self,
            session,
            pipeline):


        for candle in session["candles"]:


            try:


                result = pipeline.process(
                    candle
                )


                session["signals"].append(
                    result
                )


                session["processed"] += 1



            except Exception as error:


                print(
                    "REPLAY ERROR:",
                    error
                )



            time.sleep(0.01)



        return self.summary(
            session
        )






    def summary(self, session):


        return {


            "session_id":

            session["id"],


            "symbol":

            session["symbol"],


            "candles_processed":

            session["processed"],


            "signals":

            len(
                session["signals"]
            ),


            "completed":

            True,


            "time":

            str(datetime.utcnow())

        }






    def latest(self):


        if self.sessions:

            return self.sessions[-1]


        return None
