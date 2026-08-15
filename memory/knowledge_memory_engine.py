"""
=========================================================

GSIS INSTITUTIONAL

KNOWLEDGE MEMORY ENGINE

Version 1.0

Institutional Memory Layer

=========================================================
"""


from datetime import datetime
import uuid



class KnowledgeMemoryEngine:


    def __init__(self):

        self.name = "Knowledge Memory Engine"

        self.status = "CREATED"

        self.market_memory = []

        self.decision_memory = []

        self.strategy_memory = []

        self.system_events = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("KNOWLEDGE MEMORY ENGINE ONLINE")
        print("==============================")





    def store_market_event(
            self,
            asset,
            condition,
            observation):


        data = {

            "id":
            str(uuid.uuid4()),

            "asset":
            asset,

            "condition":
            condition,

            "observation":
            observation,

            "time":
            str(datetime.utcnow())

        }


        self.market_memory.append(data)


        return data






    def store_decision(
            self,
            action,
            reason,
            outcome):


        data = {

            "action":
            action,

            "reason":
            reason,

            "outcome":
            outcome,

            "time":
            str(datetime.utcnow())

        }


        self.decision_memory.append(data)


        return data






    def store_strategy(
            self,
            strategy,
            performance):


        data = {

            "strategy":
            strategy,

            "performance":
            performance,

            "time":
            str(datetime.utcnow())

        }


        self.strategy_memory.append(data)


        return data






    def memory_report(self):


        return {


            "status":
            self.status,


            "market_records":
            len(self.market_memory),


            "decisions":
            len(self.decision_memory),


            "strategies":
            len(self.strategy_memory)

        }
