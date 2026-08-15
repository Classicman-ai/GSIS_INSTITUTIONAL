"""
=========================================================
GSIS INSTITUTIONAL

DATA BUS &
INTERNAL COMMUNICATION ARCHITECTURE ENGINE

Version 1.0

System Communication Layer

=========================================================
"""


from datetime import datetime
import uuid



class DataBusEngine:


    def __init__(self):

        self.name = "GSIS Data Bus Engine"

        self.status = "CREATED"

        self.channels = []

        self.messages = []

        self.subscribers = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DATA BUS ENGINE ONLINE")
        print("==============================")





    def create_channel(
            self,
            name):


        channel = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "time":

            str(datetime.utcnow())

        }



        self.channels.append(channel)


        return channel






    def subscribe(
            self,
            engine,
            channel):


        subscription = {


            "engine":

            engine,


            "channel":

            channel,


            "time":

            str(datetime.utcnow())

        }



        self.subscribers.append(subscription)


        return subscription






    def publish(
            self,
            source,
            event,
            data):


        message = {


            "id":

            str(uuid.uuid4()),


            "source":

            source,


            "event":

            event,


            "data":

            data,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(message)


        return message






    def bus_report(self):


        return {


            "status":

            self.status,


            "channels":

            len(self.channels),


            "messages":

            len(self.messages),


            "subscribers":

            len(self.subscribers)

        }
