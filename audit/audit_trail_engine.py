"""
=========================================================
GSIS INSTITUTIONAL

AUDIT TRAIL &
COMPLIANCE INTELLIGENCE ENGINE

Version 1.0

Transparency Layer

=========================================================
"""


from datetime import datetime
import uuid



class AuditTrailEngine:


    def __init__(self):

        self.name = "Audit Trail Engine"

        self.status = "CREATED"

        self.records = []

        self.reports = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("AUDIT TRAIL ENGINE ONLINE")
        print("==============================")





    def record_event(
            self,
            category,
            event,
            source):


        record = {


            "id":

            str(uuid.uuid4()),


            "category":

            category,


            "event":

            event,


            "source":

            source,


            "time":

            str(datetime.utcnow())

        }



        self.records.append(record)


        return record






    def search_records(
            self,
            keyword):


        results = []


        for record in self.records:

            if keyword.lower() in str(record).lower():

                results.append(record)



        return results






    def create_report(
            self,
            title):


        report = {


            "title":

            title,


            "records":

            len(self.records),


            "time":

            str(datetime.utcnow())

        }



        self.reports.append(report)


        return report






    def audit_report(self):


        return {


            "status":

            self.status,


            "records":

            len(self.records),


            "reports":

            len(self.reports)

        }
