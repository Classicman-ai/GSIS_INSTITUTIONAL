"""
=========================================================
GSIS INSTITUTIONAL
Core Orchestrator
Version: 1.0
=========================================================
"""

import time


class Orchestrator:
    def __init__(self):
        self.engines = []

    def register_engine(self, engine):
        print(f"[REGISTER] {engine.name}")
        self.engines.append(engine)

    def initialize(self):
        print("\n========== GSIS INITIALIZATION ==========")
        for engine in self.engines:
            engine.initialize()

    def run(self):
        print("\n========== GSIS RUNNING ==========")
        while True:
            for engine in self.engines:
                engine.run()

            time.sleep(1)

    def shutdown(self):
        print("\n========== GSIS SHUTDOWN ==========")
        for engine in self.engines:
            engine.shutdown()
