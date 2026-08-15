"""
GSIS ENGINE REGISTRY
VERSION 1.0

Central management system for all GSIS engines
"""

from core.logger import Logger


class EngineRegistry:


    def __init__(self):

        self.logger = Logger("ENGINE_REGISTRY")

        self.engines = {}



    def register(self, engine):

        name = engine.engine_name

        self.engines[name] = {

            "object": engine,

            "version": engine.version,

            "status": "REGISTERED"

        }


        self.logger.info(
            f"{name} REGISTERED"
        )



    def start_all(self):

        self.logger.info(
            "STARTING ALL ENGINES"
        )


        for name, data in self.engines.items():

            engine = data["object"]

            engine.start()

            data["status"] = "RUNNING"



    def stop_all(self):

        for name, data in self.engines.items():

            data["status"] = "STOPPED"



        self.logger.info(
            "ALL ENGINES STOPPED"
        )



    def status(self):

        result = {}


        for name, data in self.engines.items():

            result[name] = {

                "version": data["version"],

                "status": data["status"]

            }


        return result



if __name__ == "__main__":


    print("===================================")
    print("GSIS ENGINE REGISTRY")
    print("VERSION 1.0")
    print("===================================")


    registry = EngineRegistry()


    print(
        registry.status()
    )


    print(
        "ENGINE REGISTRY READY"
    )
