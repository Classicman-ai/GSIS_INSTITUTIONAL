"""
=========================================================
GSIS INSTITUTIONAL SYSTEM
Main Controller
Version: 2.0

Modular Quantitative Intelligence Platform
=========================================================
"""


from core.engine_manager import EngineManager



class GSISInstitutional:


    def __init__(self):

        self.engine_manager = EngineManager()



    def start(self):

        print(
            "======================================"
        )

        print(
            "        GSIS INSTITUTIONAL"
        )

        print(
            " Quantitative Intelligence System"
        )

        print(
            "======================================"
        )


        self.engine_manager.start()



    def stop(self):

        self.engine_manager.stop()



if __name__ == "__main__":


    system = GSISInstitutional()


    try:

        system.start()


    except KeyboardInterrupt:

        system.stop()
