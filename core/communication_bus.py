"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL INTEGRATION &
COMMUNICATION BUS (IICB)

Version: 1.0

Central communication layer

Functions:
- Event routing
- Engine communication
- Message logging
- Event broadcasting

=========================================================
"""


from datetime import datetime
import uuid



class CommunicationBus:


    def __init__(self):

        self.name = "Institutional Communication Bus"

        self.status = "CREATED"

        self.subscribers = {}

        self.event_history = []



    def initialize(self):

        self.status = "ONLINE"


        print("==============================")

        print(
            "COMMUNICATION BUS ONLINE"
        )

        print("==============================")



    def subscribe(
            self,
            event,
            engine):


        if event not in self.subscribers:

            self.subscribers[event] = []


        self.subscribers[event].append(
            engine
        )


        print(
            "SUBSCRIBED:",
            engine,
            "TO",
            event
        )



    def publish(
            self,
            event,
            data):


        event_id = str(
            uuid.uuid4()
        )


        message = {


            "event_id":

            event_id,


            "event":

            event,


            "timestamp":

            str(datetime.utcnow()),


            "data":

            data

        }


        self.event_history.append(
            message
        )


        print("==============================")

        print(
            "EVENT:",
            event
        )

        print(
            "ID:",
            event_id
        )

        print("==============================")



        listeners = self.subscribers.get(
            event,
            []
        )


        for engine in listeners:


            try:


                engine.update(
                    data
                )


            except Exception as error:


                print(
                    "BUS DELIVERY ERROR:",
                    error
                )



        return message



    def get_history(self):


        return self.event_history



    def shutdown(self):


        self.status = "OFFLINE"


        print(
            "COMMUNICATION BUS STOPPED"
        )
