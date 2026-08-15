"""
=========================================================
GSIS INSTITUTIONAL

AUTHENTICATION & SECURITY ENGINE

Version 1.0

Institutional Security Control Layer

=========================================================
"""


from datetime import datetime
import uuid
import hashlib



class SecurityEngine:


    def __init__(self):

        self.name = "Security Engine"

        self.status = "CREATED"

        self.users = {}

        self.sessions = {}

        self.audit_log = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SECURITY ENGINE ONLINE")
        print("==============================")





    def create_user(
            self,
            username,
            password,
            role):


        password_hash = hashlib.sha256(

            password.encode()

        ).hexdigest()



        self.users[username] = {


            "password":

            password_hash,


            "role":

            role,


            "created":

            str(datetime.utcnow())

        }



        return {


            "status":

            "USER CREATED",


            "username":

            username

        }






    def authenticate(
            self,
            username,
            password):


        if username not in self.users:


            return {

                "status":

                "FAILED"

            }



        password_hash = hashlib.sha256(

            password.encode()

        ).hexdigest()



        if self.users[username]["password"] == password_hash:


            token = str(uuid.uuid4())


            self.sessions[token] = username



            self.log_event(

                username,

                "LOGIN SUCCESS"

            )



            return {


                "status":

                "AUTHORIZED",


                "token":

                token

            }



        self.log_event(

            username,

            "LOGIN FAILED"

        )


        return {


            "status":

            "FAILED"

        }






    def check_permission(
            self,
            token,
            required_role):


        if token not in self.sessions:


            return False



        username = self.sessions[token]


        role = self.users[username]["role"]



        if role == "SYSTEM_OWNER":


            return True



        return role == required_role






    def log_event(
            self,
            user,
            action):


        self.audit_log.append({


            "time":

            str(datetime.utcnow()),


            "user":

            user,


            "action":

            action

        })






    def security_report(self):


        return {


            "users":

            len(self.users),


            "active_sessions":

            len(self.sessions),


            "events":

            len(self.audit_log),


            "status":

            self.status

        }
