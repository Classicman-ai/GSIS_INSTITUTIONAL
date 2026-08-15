"""
=========================================================
GSIS INSTITUTIONAL

SECURITY & ACCESS CONTROL INTELLIGENCE ENGINE

Version 1.0

Institutional Security Layer

=========================================================
"""


from datetime import datetime
import uuid



class SecurityAccessEngine:


    def __init__(self):

        self.name = "Security Access Engine"

        self.status = "CREATED"

        self.users = {}

        self.permissions = {}

        self.security_logs = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SECURITY ACCESS ENGINE ONLINE")
        print("==============================")





    def create_user(
            self,
            username,
            role):


        user = {


            "id":

            str(uuid.uuid4()),


            "username":

            username,


            "role":

            role,


            "created":

            str(datetime.utcnow())

        }


        self.users[username] = user


        return user






    def assign_permission(
            self,
            role,
            permission):


        if role not in self.permissions:

            self.permissions[role] = []



        self.permissions[role].append(
            permission
        )


        return {


            "role":

            role,


            "permission":

            permission

        }






    def check_access(
            self,
            role,
            action):


        allowed = self.permissions.get(
            role,
            []
        )


        result = {


            "role":

            role,


            "action":

            action,


            "status":

            "DENIED"

        }



        if action in allowed:

            result["status"] = "GRANTED"



        self.security_logs.append({

            "event":

            result,


            "time":

            str(datetime.utcnow())

        })



        return result






    def security_report(self):


        return {


            "status":

            self.status,


            "users":

            len(self.users),


            "roles":

            len(self.permissions),


            "security_events":

            len(self.security_logs)

        }
