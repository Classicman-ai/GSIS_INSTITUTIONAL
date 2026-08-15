"""
=========================================================
GSIS INSTITUTIONAL

CONFIGURATION & ENVIRONMENT MANAGEMENT ENGINE

Version 1.0

Central System Configuration Layer

=========================================================
"""


from datetime import datetime
import uuid



class ConfigurationEngine:


    def __init__(self):

        self.name = "Configuration Engine"

        self.status = "CREATED"

        self.configurations = {}

        self.environments = {}

        self.history = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("CONFIGURATION ENGINE ONLINE")
        print("==============================")





    def create_environment(
            self,
            name,
            settings):


        environment = {


            "id":

            str(uuid.uuid4()),


            "name":

            name,


            "settings":

            settings,


            "created":

            str(datetime.utcnow())

        }



        self.environments[name] = environment


        return environment






    def set_parameter(
            self,
            name,
            value):


        old_value = self.configurations.get(
            name
        )



        self.configurations[name] = value



        self.history.append({


            "parameter":

            name,


            "old":

            old_value,


            "new":

            value,


            "time":

            str(datetime.utcnow())

        })



        return {


            "parameter":

            name,


            "value":

            value

        }






    def get_parameter(
            self,
            name):


        return self.configurations.get(
            name,
            None
        )






    def load_environment(
            self,
            name):


        return self.environments.get(
            name,
            None
        )






    def configuration_report(self):


        return {


            "status":

            self.status,


            "parameters":

            len(self.configurations),


            "environments":

            len(self.environments),


            "changes":

            len(self.history)

        }
