"""
=========================================================
GSIS INSTITUTIONAL

CONFIGURATION MANAGEMENT &
ENVIRONMENT CONTROL INTELLIGENCE ENGINE

Version 1.0

System Control Layer

=========================================================
"""


from datetime import datetime
import uuid



class ConfigurationManagementEngine:


    def __init__(self):

        self.name = "Configuration Management Engine"

        self.status = "CREATED"

        self.configurations = []

        self.versions = []

        self.environments = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("CONFIGURATION MANAGEMENT ENGINE ONLINE")
        print("==============================")





    def create_configuration(
            self,
            name,
            value):


        config = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "value":

            value,


            "time":

            str(datetime.utcnow())

        }



        self.configurations.append(config)


        return config






    def create_version(
            self,
            version,
            change):


        data = {


            "version":

            version,


            "change":

            change,


            "time":

            str(datetime.utcnow())

        }



        self.versions.append(data)


        return data






    def register_environment(
            self,
            name):


        environment = {


            "name":

            name,


            "status":

            "ACTIVE",


            "time":

            str(datetime.utcnow())

        }



        self.environments.append(environment)


        return environment






    def configuration_report(self):


        return {


            "status":

            self.status,


            "configurations":

            len(self.configurations),


            "versions":

            len(self.versions),


            "environments":

            len(self.environments)

        }
