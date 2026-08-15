"""
=========================================================
GSIS INSTITUTIONAL
Base Engine
Version: 1.0
=========================================================
"""


class BaseEngine:
    """
    Base class for all GSIS Institutional engines.
    Every engine should inherit from this class.
    """

    def __init__(self, name):
        self.name = name
        self.status = "CREATED"

    def initialize(self):
        self.status = "INITIALIZED"
        print(f"[{self.name}] Initialized")

    def run(self):
        self.status = "RUNNING"
        print(f"[{self.name}] Running")

    def shutdown(self):
        self.status = "STOPPED"
        print(f"[{self.name}] Shutdown")

    def health_check(self):
        return {
            "engine": self.name,
            "status": self.status
        }

    def reset(self):
        self.status = "RESET"
        print(f"[{self.name}] Reset")

    def get_status(self):
        return self.status
