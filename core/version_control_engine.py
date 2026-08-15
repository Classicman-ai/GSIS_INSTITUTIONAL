"""
=========================================================
GSIS INSTITUTIONAL

VERSION CONTROL & DEPLOYMENT INTELLIGENCE ENGINE

Version 1.0

Software Lifecycle Management Layer

=========================================================
"""


from datetime import datetime
import uuid



class VersionControlEngine:


    def __init__(self):

        self.name = "Version Control Engine"

        self.status = "CREATED"

        self.versions = []

        self.deployments = []

        self.releases = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("VERSION CONTROL ENGINE ONLINE")
        print("==============================")





    def create_version(
            self,
            version,
            description):


        record = {


            "id":

            str(uuid.uuid4()),


            "version":

            version,


            "description":

            description,


            "created":

            str(datetime.utcnow())

        }



        self.versions.append(record)


        return record






    def create_release(
            self,
            module,
            version,
            status):


        release = {


            "module":

            module,


            "version":

            version,


            "status":

            status,


            "time":

            str(datetime.utcnow())

        }



        self.releases.append(release)


        return release






    def deploy(
            self,
            version,
            environment):


        deployment = {


            "version":

            version,


            "environment":

            environment,


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


        return {


            "rollback_to":

            version,


            "status":

            "COMPLETED",


            "time":

            str(datetime.utcnow())

        }






    def version_report(self):


        return {


            "status":

            self.status,


            "versions":

            len(self.versions),


            "releases":

            len(self.releases),


            "deployments":

            len(self.deployments)

        }
