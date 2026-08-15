"""
=========================================================
GSIS INSTITUTIONAL
MARKET MEMORY CONNECTOR
Version: 1.0

Historical + Live Data Integration Layer
=========================================================
"""


from database.market_memory import MarketMemoryDatabase



class MemoryConnector:


    def __init__(self):

        self.memory = MarketMemoryDatabase()

        self.status = "CREATED"



    def initialize(self):

        self.memory.initialize()

        self.status = "ONLINE"

        print(
            "MEMORY CONNECTOR ONLINE"
        )



    def store_market_state(
            self,
            state):


        memory_id = (

            self.memory.create_memory(

                state

            )

        )


        return memory_id



    def store_historical_data(
            self,
            historical_records):


        count = 0


        for record in historical_records:


            self.store_market_state(

                record

            )


            count += 1



        print(

            "HISTORICAL RECORDS STORED:",

            count

        )


        return count



    def close(self):

        self.memory.close()
