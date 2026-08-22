"""Compatibility facade for the canonical autonomous GSIS runtime.

There is one production orchestrator now: GSISUnifiedEngine. This module keeps
legacy imports working without maintaining a second execution pipeline.
"""

from institutional import GSISConfig, GSISUnifiedEngine


class GSISMasterOrchestrator:
    """Legacy name mapped to the single canonical runtime."""

    def __init__(self, config=None):
        self.config = config or GSISConfig.from_env()
        self.engine = GSISUnifiedEngine(self.config)

    def validate_runtime(self):
        return self.engine.validate_runtime()

    def cycle(self):
        return self.engine.cycle()

    def run_forever(self):
        return self.engine.run_forever()


if __name__ == "__main__":
    GSISMasterOrchestrator().run_forever()
