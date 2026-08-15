"""
=========================================================
GSIS INSTITUTIONAL

SECURITY & PERMISSION CONTROL ENGINE

Version 1.0

Institutional Safety Governance Layer

=========================================================
"""


from datetime import datetime



class SecurityPermissionEngine:


    def __init__(self):

        self.name = "Security Permission Engine"

        self.status = "CREATED"

        self.mode = "RESEARCH"

        self.execution_allowed = False

        self.risk_lock = False

        self.emergency_stop = False

        self.permissions = {}





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("SECURITY PERMISSION ENGINE ONLINE")
        print("==============================")





    def set_mode(self, mode):


        allowed = [

            "RESEARCH",

            "SIMULATION",

            "LIVE"

        ]


        if mode in allowed:


            self.mode = mode


            if mode == "LIVE":

                self.execution_allowed = True


            else:

                self.execution_allowed = False



        return self.status_report()






    def grant_permission(
            self,
            engine_name):


        self.permissions[engine_name] = True


        return {


            "engine":

            engine_name,


            "permission":

            "GRANTED"

        }






    def revoke_permission(
            self,
            engine_name):


        self.permissions[engine_name] = False


        return {


            "engine":

            engine_name,


            "permission":

            "REVOKED"

        }






    def check_execution(self):


        if self.emergency_stop:

            return False



        if self.risk_lock:

            return False



        if not self.execution_allowed:

            return False



        return True






    def activate_emergency_stop(self):


        self.emergency_stop = True


        self.execution_allowed = False






    def release_emergency_stop(self):


        self.emergency_stop = False






    def activate_risk_lock(self):


        self.risk_lock = True






    def release_risk_lock(self):


        self.risk_lock = False






    def status_report(self):


        return {


            "timestamp":

            str(datetime.utcnow()),


            "mode":

            self.mode,


            "execution":

            self.check_execution(),


            "risk_lock":

            self.risk_lock,


            "emergency_stop":

            self.emergency_stop


        }
