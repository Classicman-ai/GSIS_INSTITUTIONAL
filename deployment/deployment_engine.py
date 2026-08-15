"""
=========================================================
GSIS INSTITUTIONAL

DEPLOYMENT &
CONTINUOUS INTEGRATION INTELLIGENCE ENGINE

Version 1.0

Software Lifecycle Layer

=========================================================
"""


from datetime import datetime
import uuid



class DeploymentEngine:


    def __init__(self):

        self.name = "Deployment Intelligence Engine"

        self.status = "CREATED"

        self.releases = []

        self.tests = []

        self.deployments = []

        self.rollbacks = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DEPLOYMENT ENGINE ONLINE")
        print("==============================")





    def create_release(
            self,
            component,
            version):


        release = {


            "id":

            str(uuid.uuid4()),


            "component":

            component,


            "version":

            version,


            "time":

            str(datetime.utcnow())

        }



        self.releases.append(release)


        return release






    def run_test(
            self,
            component,
            result):


        test = {


            "component":

            component,


            "result":

            result,


            "time":

            str(datetime.utcnow())

        }



        self.tests.append(test)


        return test






    def deploy(
            self,
            component,
            version):


        deployment = {


            "component":

            component,


            "version":

            version,


            "status":

            "DEPLOYED",


            "time":

            str(datetime.utcnow())

        }



        self.deployments.append(deployment)


        return deployment






    def rollback(
            self,
            version):


        rollback = {


            "version":

            version,


            "status":

            "RESTORED",


            "time":

            str(datetime.utcnow())

        }



        self.rollbacks.append(rollback)


        return rollback






    def deployment_report(self):


        return {


            "status":

            self.status,


            "releases":

            len(self.releases),


            "tests":

            len(self.tests),


            "deployments":

            len(self.deployments),


            "rollbacks":

            len(self.rollbacks)

        }
