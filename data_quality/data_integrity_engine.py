"""
=========================================================
GSIS INSTITUTIONAL

DATA INTEGRITY & MARKET DATA QUALITY
INTELLIGENCE ENGINE

Version 1.0

Data Validation Layer

=========================================================
"""


from datetime import datetime
import uuid



class DataIntegrityEngine:


    def __init__(self):

        self.name = "Data Integrity Engine"

        self.status = "CREATED"

        self.validations = []

        self.errors = []

        self.sources = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DATA INTEGRITY ENGINE ONLINE")
        print("==============================")





    def validate_data(
            self,
            symbol,
            status,
            details):


        record = {


            "id":

            str(uuid.uuid4()),


            "symbol":

            symbol,


            "status":

            status,


            "details":

            details,


            "time":

            str(datetime.utcnow())

        }



        self.validations.append(record)


        return record






    def record_error(
            self,
            error_type,
            description):


        error = {


            "error":

            error_type,


            "description":

            description,


            "time":

            str(datetime.utcnow())

        }



        self.errors.append(error)


        return error






    def register_source(
            self,
            source,
            reliability):


        data = {


            "source":

            source,


            "reliability":

            reliability,


            "time":

            str(datetime.utcnow())

        }



        self.sources.append(data)


        return data






    def integrity_report(self):


        return {


            "status":

            self.status,


            "validations":

            len(self.validations),


            "errors":

            len(self.errors),


            "sources":

            len(self.sources)

        }
