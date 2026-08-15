"""
=========================================================
GSIS INSTITUTIONAL

MARKET SENTIMENT & BEHAVIORAL
INTELLIGENCE ENGINE

Version 1.0

Market Psychology Layer

=========================================================
"""


from datetime import datetime
import uuid



class SentimentBehaviorEngine:


    def __init__(self):

        self.name = "Sentiment Behavior Engine"

        self.status = "CREATED"

        self.sentiment_records = []

        self.behavior_events = []

        self.extremes = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SENTIMENT BEHAVIOR ENGINE ONLINE")
        print("==============================")





    def record_sentiment(
            self,
            asset,
            sentiment,
            score):


        record = {


            "id":

            str(uuid.uuid4()),


            "asset":

            asset,


            "sentiment":

            sentiment,


            "score":

            score,


            "time":

            str(datetime.utcnow())

        }



        self.sentiment_records.append(record)


        return record






    def record_behavior(
            self,
            behavior,
            interpretation):


        event = {


            "behavior":

            behavior,


            "interpretation":

            interpretation,


            "time":

            str(datetime.utcnow())

        }



        self.behavior_events.append(event)


        return event






    def detect_extreme(
            self,
            condition,
            level):


        extreme = {


            "condition":

            condition,


            "level":

            level,


            "time":

            str(datetime.utcnow())

        }



        self.extremes.append(extreme)


        return extreme






    def sentiment_report(self):


        return {


            "status":

            self.status,


            "sentiment_records":

            len(self.sentiment_records),


            "behavior_events":

            len(self.behavior_events),


            "extremes":

            len(self.extremes)

        }
