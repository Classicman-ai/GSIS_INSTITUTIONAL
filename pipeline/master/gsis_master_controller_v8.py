from core.engine_loader import EngineLoader
from core.gsis_pipeline import GSISPipeline
from adapters.modular_engine import ModularEngine

from engines.data.market_data_engine import MarketDataEngine
from engines.liquidity.liquidity_engine import LiquidityEngine
from engines.volume.volume_intelligence import VolumeIntelligence
from engines.orderflow.order_flow_engine import OrderFlowEngine
from engines.regime.regime_intelligence_engine import RegimeIntelligenceEngine
from engines.adaptive.adaptive_market_intelligence import AdaptiveMarketIntelligence
from engines.validation.market_validation_engine import MarketValidationEngine
from engines.fusion.decision_fusion_engine import DecisionFusionEngine
from engines.signals.signal_generator import SignalGenerator
from engines.risk.risk_engine import RiskEngine
from engines.quality.trade_quality_gate import TradeQualityGate
from engines.execution.execution_engine import ExecutionEngine
from engines.journal.journal_engine import JournalEngine
from engines.performance.performance_engine import PerformanceEngine
from engines.memory.memory_engine import MemoryEngine
from engines.intelligence.trade_intelligence_engine import TradeIntelligenceEngine


class GSISMasterControllerV8:


    def __init__(self):

        self.loader = EngineLoader()

        self.pipeline = GSISPipeline(
            "BTCUSDT"
        )


        self.engines = [

            ModularEngine("MARKET", MarketDataEngine()),
            ModularEngine("LIQUIDITY", LiquidityEngine()),
            ModularEngine("VOLUME", VolumeIntelligence()),
            ModularEngine("ORDERFLOW", OrderFlowEngine()),
            ModularEngine("REGIME", RegimeIntelligenceEngine()),
            ModularEngine("ADAPTIVE", AdaptiveMarketIntelligence()),
            ModularEngine("VALIDATION", MarketValidationEngine()),
            ModularEngine("FUSION", DecisionFusionEngine()),
            ModularEngine("SIGNAL", SignalGenerator()),
            ModularEngine("RISK", RiskEngine()),
            ModularEngine("QUALITY", TradeQualityGate()),
            ModularEngine("EXECUTION", ExecutionEngine()),
            ModularEngine("JOURNAL", JournalEngine()),
            ModularEngine("PERFORMANCE", PerformanceEngine()),
            ModularEngine("MEMORY", MemoryEngine()),
            ModularEngine("INTELLIGENCE", TradeIntelligenceEngine())

        ]


    def update_context(self, result):

        name = result.get(
            "engine",
            ""
        ).lower()


        mapping = {

            "market data": "market",
            "liquidity": "liquidity",
            "volume": "volume",
            "order flow": "orderflow",
            "regime": "regime",
            "adaptive": "adaptive",
            "validation": "validation",
            "fusion": "fusion",
            "signal": "signal",
            "risk": "risk",
            "quality": "quality",
            "execution": "execution",
            "journal": "journal",
            "performance": "performance",
            "memory": "memory",
            "intelligence": "intelligence"

        }


        for key, value in mapping.items():

            if key in name:

                self.pipeline.runner.update(
                    value,
                    result
                )

                break



    def run(self):

        print("===============================")
        print("GSIS MASTER CONTROLLER v9.0")
        print("===============================")


        for engine in self.engines:

            try:

                result = engine.execute(
                    self.pipeline.runner.context
                )


                print()
                print(result)


                if isinstance(result, dict):

                    self.update_context(
                        result
                    )


            except Exception as e:

                print(
                    {
                        "engine": engine.name,
                        "status": "ERROR",
                        "error": str(e)
                    }
                )


        print("===============================")
        print("GSIS PIPELINE COMPLETE")
        print("===============================")



if __name__ == "__main__":

    controller = GSISMasterControllerV8()

    controller.run()
