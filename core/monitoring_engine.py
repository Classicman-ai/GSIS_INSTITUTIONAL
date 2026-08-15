"""
=========================================================
GSIS INSTITUTIONAL

INSTITUTIONAL MONITORING
& ALERT SYSTEM (IMAS)

Monitoring Engine v1.1

Functions:
- Engine health tracking
- Event listening
- Event history
- Alert generation
- System status reporting

=========================================================
"""


from datetime import datetime



class MonitoringEngine:


    def __init__(self):


        self.name = "Institutional Monitoring Engine"

        self.status = "CREATED"

        self.engines = {}

        self.events = []

        self.alerts = []

        self.event_counter = 0



    def initialize(self):


        self.status = "ONLINE"


        print("==============================")

        print(
            "MONITORING ENGINE ONLINE"
        )

        print("==============================")



    def update(self, data):

        """
        Communication Bus listener
        """

        self.record_event(
            "BUS_EVENT",
            data
        )



    def register_engine(
            self,
            engine_name):


        self.engines[engine_name] = {

            "status":
            "ONLINE",

            "last_update":
            str(datetime.utcnow())

        }


        print(
            "MONITORED:",
            engine_name
        )



    def heartbeat(
            self,
            engine_name):


        if engine_name in self.engines:


            self.engines[engine_name]["last_update"] = (
                str(datetime.utcnow())
            )


            self.engines[engine_name]["status"] = "ONLINE"



    def record_event(
            self,
            event,
            data=None):


        self.event_counter += 1


        entry = {


            "id":
            self.event_counter,


            "event":
            event,


            "time":
            str(datetime.utcnow()),


            "data":
            data

        }


        self.events.append(entry)



        print(
            "MONITOR EVENT:",
            event
        )



    def create_alert(
            self,
            level,
            message):


        alert = {


            "level":
            level,


            "message":
            message,


            "time":
            str(datetime.utcnow())

        }


        self.alerts.append(alert)



        print("==============================")

        print(
            "ALERT:",
            level
        )

        print(
            message
        )

        print("==============================")



    def system_health(self):


        total = len(self.engines)


        online = 0


        for engine in self.engines.values():


            if engine["status"] == "ONLINE":

                online += 1



        if total == 0:

            score = 0

        else:

            score = int(
                (online / total) * 100
            )



        return {


            "health_score":
            score,


            "engines_total":
            total,


            "engines_online":
            online,


            "events_processed":
            self.event_counter

        }



    def report(self):


        return {


            "system":
            "GSIS",


            "status":
            self.status,


            "health":
            self.system_health(),


            "alerts":
            len(self.alerts)

        }
