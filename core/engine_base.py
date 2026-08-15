"""
GSIS CORE ENGINE BASE
VERSION 1.0

Foundation class for all GSIS engines
"""

import time

from core.database import Database
from core.logger import Logger
from core.config import SYSTEM_NAME, SYSTEM_VERSION



class EngineBase:


    def __init__(self, engine_name, version="1.0"):

        self.engine_name = engine_name

        self.version = version

        self.database = Database()

        self.logger = Logger(engine_name)

        self.start_time = None



    def start(self):

        self.start_time = time.time()

        self.logger.info(
            f"{self.engine_name} STARTED"
        )


        self.logger.info(
            f"GSIS VERSION {SYSTEM_VERSION}"
        )



    def finish(self):

        runtime = (
            time.time()
            -
            self.start_time
        )


        self.logger.info(
            f"{self.engine_name} COMPLETED"
        )


        self.logger.info(
            f"Runtime: {round(runtime,3)} seconds"
        )



    def error(self, message):

        self.logger.error(message)



    def status(self):

        return {

            "engine": self.engine_name,

            "version": self.version,

            "status": "READY"

        }



    def run(self):

        raise NotImplementedError(
            "Engine must implement run()"
        )



if __name__ == "__main__":


    print("===================================")
    print("GSIS ENGINE BASE")
    print("VERSION 1.0")
    print("===================================")



    engine = EngineBase(
        "TEST_ENGINE"
    )


    engine.start()


    print(
        engine.status()
    )


    engine.finish()


    print("ENGINE BASE READY")
