"""
GSIS ADAPTER MANAGER
VERSION 2.0
"""

from core.logger import Logger

from engines.adapters.regime_adapter import RegimeAdapter

from engines.adapters.intelligence_adapter import IntelligenceAdapter



class AdapterManager:


    def __init__(self, registry):

        self.registry = registry

        self.logger = Logger(
            "ADAPTER_MANAGER"
        )



    def load_all(self):

        self.logger.info(
            "LOADING GSIS ADAPTERS"
        )


        engines = [

            RegimeAdapter(),

            IntelligenceAdapter()

        ]


        for engine in engines:

            self.registry.register(
                engine
            )


        self.logger.info(
            "GSIS ADAPTERS ONLINE"
        )
