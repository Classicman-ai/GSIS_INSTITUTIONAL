"""
GSIS MASTER CONTROLLER
VERSION 2.0

Central orchestration layer for GSIS
"""

import time

from core.logger import Logger
from core.engine_registry import EngineRegistry
from engines.adapter_manager import AdapterManager


class GSISController:


    def __init__(self):

        self.logger = Logger(
            "GSIS_CONTROLLER"
        )

        self.registry = EngineRegistry()

        self.adapter_manager = AdapterManager(
            self.registry
        )

        self.system_status = "OFFLINE"

        self.version = "2.0"



    def boot(self):

        print("===================================")
        print("GSIS MASTER CONTROLLER")
        print("VERSION", self.version)
        print("SYSTEM BOOT SEQUENCE")
        print("===================================")


        self.logger.info(
            "GSIS BOOT INITIALIZED"
        )


        # Load engine adapters

        self.adapter_manager.load_all()


        self.system_status = "ONLINE"


        self.logger.info(
            "GSIS SYSTEM ONLINE"
        )



    def engine_health(self):

        print("-----------------------------------")
        print("GSIS ENGINE HEALTH")
        print("-----------------------------------")


        status = self.registry.status()


        if not status:

            print(
                "NO ENGINES REGISTERED"
            )


        else:

            for name,data in status.items():

                print(
                    name,
                    " | VERSION:",
                    data["version"],
                    "| STATUS:",
                    data["status"]
                )


        print("-----------------------------------")



    def system_state(self):

        return {

            "system":

                "GSIS",

            "version":

                self.version,

            "status":

                self.system_status,

            "engines":

                len(self.registry.engines)

        }



    def shutdown(self):

        self.logger.info(
            "GSIS SHUTDOWN REQUESTED"
        )


        self.registry.stop_all()


        self.system_status = "OFFLINE"



if __name__ == "__main__":


    controller = GSISController()


    controller.boot()


    time.sleep(1)


    controller.engine_health()


    print(
        controller.system_state()
    )


    print("-----------------------------------")
    print("GSIS CONTROLLER READY")
    print("-----------------------------------")
