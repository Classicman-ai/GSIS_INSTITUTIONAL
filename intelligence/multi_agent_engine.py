"""
=========================================================
GSIS INSTITUTIONAL

MULTI-AGENT INTELLIGENCE COORDINATION ENGINE

Version 1.0

AI Organization Layer

=========================================================
"""


from datetime import datetime
import uuid



class MultiAgentEngine:


    def __init__(self):

        self.name = "Multi Agent Intelligence Engine"

        self.status = "CREATED"

        self.agents = {}

        self.messages = []

        self.decisions = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("MULTI-AGENT ENGINE ONLINE")
        print("==============================")





    def register_agent(
            self,
            name,
            role):


        agent = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "role":

            role,


            "created":

            str(datetime.utcnow())

        }



        self.agents[name] = agent


        return agent






    def send_message(
            self,
            sender,
            receiver,
            message):


        communication = {


            "sender":

            sender,


            "receiver":

            receiver,


            "message":

            message,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(
            communication
        )


        return communication






    def create_decision(
            self,
            decision,
            agents_supporting):


        result = {


            "decision":

            decision,


            "support":

            agents_supporting,


            "time":

            str(datetime.utcnow())

        }



        self.decisions.append(result)


        return result






    def agent_report(self):


        return {


            "status":

            self.status,


            "agents":

            len(self.agents),


            "messages":

            len(self.messages),


            "decisions":

            len(self.decisions)

        }
