"""
=========================================================
GSIS INSTITUTIONAL

AUDIT TRAIL INTELLIGENCE ENGINE

Version 1.0

Institutional Record Keeping Layer

=========================================================
"""


from datetime import datetime
import uuid



class AuditTrailEngine:


    def __init__(self):

        self.name = "Audit Trail Engine"

        self.status = "CREATED"

        self.records = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("AUDIT TRAIL ENGINE ONLINE")
        print("==============================")





    def record_event(
            self,
            event_type,
            source,
            details):


        record = {


            "id":

            str(uuid.uuid4()),


            "event_type":

            event_type,


            "source":

            source,


            "details":

            details,


            "timestamp":

            str(datetime.utcnow())

        }



        self.records.append(record)


        return record






    def search_events(
            self,
            event_type):


        return [

            record

            for record in self.records

            if record["event_type"] == event_type

        ]






    def latest_records(
            self,
            limit=10):


        return self.records[-limit:]






    def audit_report(self):


        return {


            "status":

            self.status,


            "total_records":

            len(self.records)

        }
