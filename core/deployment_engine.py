"""
=========================================================
GSIS INSTITUTIONAL

VERSION CONTROL & DEPLOYMENT ENGINE

Version 1.0

Software Lifecycle Management Layer

=========================================================
"""


from datetime import datetime



class DeploymentEngine:


    def __init__(self):

        self.name = "Deployment Engine"

        self.status = "CREATED"

        self.versions = {}

        self.deployments = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("DEPLOYMENT ENGINE ONLINE")
        print("==============================")





    def register_version(
            self,
            component,
            version):


        self.versions[component] = {


            "version":

            version,


            "registered":

            str(datetime.utcnow())

        }



        return self.versions[component]






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



        self.deployments.append(
            deployment
        )


        return deployment






    def rollback(
            self,
            component,
            previous_version):


        rollback = {


            "component":

            component,


            "restored_version":

            previous_version,


            "status":

            "ROLLED BACK",


            "time":

            str(datetime.utcnow())

        }



        self.deployments.append(
            rollback
        )


        return rollback






    def deployment_history(self):


        return self.deployments






    def system_version_report(self):


        return {


            "engine":

            self.status,


            "components":

            self.versions,


            "deployments":

            len(
                self.deployments
            )

        }
