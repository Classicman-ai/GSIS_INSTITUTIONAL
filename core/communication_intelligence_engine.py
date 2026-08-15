"""
=========================================================
GSIS INSTITUTIONAL

NOTIFICATION & COMMUNICATION INTELLIGENCE ENGINE

Version 1.0

Institutional Communication Layer

=========================================================
"""


from datetime import datetime
import uuid



class CommunicationIntelligenceEngine:


    def __init__(self):

        self.name = "Communication Intelligence Engine"

        self.status = "CREATED"

        self.channels = []

        self.messages = []

        self.events = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("COMMUNICATION INTELLIGENCE ENGINE ONLINE")
        print("==============================")





    def register_channel(
            self,
            channel):


        self.channels.append(channel)


        return {


            "status":

            "CHANNEL REGISTERED",


            "channel":

            channel

        }





    def send_message(
            self,
            title,
            message,
            priority="NORMAL"):


        data = {


            "id":

            str(uuid.uuid4()),


            "title":

            title,


            "message":

            message,


            "priority":

            priority,


            "time":

            str(datetime.utcnow())

        }



        self.messages.append(data)


        return data






    def publish_event(
            self,
            source,
            event,
            data):


        record = {


            "source":

            source,


            "event":

            event,


            "data":

            data,


            "time":

            str(datetime.utcnow())

        }



        self.events.append(record)


        return record






    def get_messages(self):


        return self.messages






    def communication_report(self):


        return {


            "status":

            self.status,


            "channels":

            len(self.channels),


            "messages":

            len(self.messages),


            "events":

            len(self.events)

        }
