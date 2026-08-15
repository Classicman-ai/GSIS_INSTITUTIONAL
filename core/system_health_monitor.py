"""
=========================================================
GSIS INSTITUTIONAL

SYSTEM HEALTH MONITORING INTELLIGENCE ENGINE

Version 1.0

Institutional Operations Center Layer

=========================================================
"""


from datetime import datetime



class SystemHealthMonitor:


    def __init__(self):

        self.name = "System Health Monitor"

        self.status = "CREATED"

        self.engines = {}

        self.alerts = []

        self.performance = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SYSTEM HEALTH MONITOR ONLINE")
        print("==============================")





    def register_engine(
            self,
            engine_name):


        self.engines[engine_name] = {


            "status":

            "UNKNOWN",


            "last_check":

            None

        }



        return self.engines[engine_name]






    def update_health(
            self,
            engine_name,
            status):


        if engine_name in self.engines:


            self.engines[engine_name]["status"] = status


            self.engines[engine_name]["last_check"] = (

                str(datetime.utcnow())

            )



        else:


            self.register_engine(
                engine_name
            )



        return self.engines[engine_name]






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


        return alert






    def record_performance(
            self,
            metric,
            value):


        data = {


            "metric":

            metric,


            "value":

            value,


            "time":

            str(datetime.utcnow())

        }



        self.performance.append(data)


        return data






    def health_report(self):


        return {


            "system":

            self.status,


            "engines":

            self.engines,


            "alerts":

            len(self.alerts),


            "performance_records":

            len(self.performance)

        }
