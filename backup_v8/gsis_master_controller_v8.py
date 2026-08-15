from core.engine_loader import EngineLoader
from core.gsis_pipeline import GSISPipeline

from adapters.modular_engine import ModularEngine

from engines.data.market_data_engine import MarketDataEngine
from engines.volume.volume_intelligence import VolumeIntelligence
from engines.orderflow.order_flow_engine import OrderFlowEngine
from engines.regime.regime_intelligence_engine import RegimeIntelligenceEngine
from engines.adaptive.adaptive_market_intelligence import AdaptiveMarketIntelligence
from engines.fusion.decision_fusion_engine import DecisionFusionEngine
from engines.signals.signal_generator import SignalGenerator
from engines.risk.risk_engine import RiskEngine
from engines.quality.trade_quality_gate import TradeQualityGate



class GSISMasterControllerV8:


    def __init__(self):

        self.loader = EngineLoader()

        self.pipeline = GSISPipeline(
            "BTCUSDT"
        )


        self.register_engines()



    def register_engines(self):

        engines = {

            "market":
            MarketDataEngine(),

            "volume":
            VolumeIntelligence(),

            "orderflow":
            OrderFlowEngine(),

            "regime":
            RegimeIntelligenceEngine(),

            "adaptive":
            AdaptiveMarketIntelligence(),

            "fusion":
            DecisionFusionEngine(),

            "signal":
            SignalGenerator(),

            "risk":
            RiskEngine(),

            "quality":
            TradeQualityGate()

        }


        for name, engine in engines.items():

            self.loader.load(
                name,
                ModularEngine(
                    name,
                    engine
                )
            )



    def run(self):

        print("===============================")
        print("GSIS MASTER CONTROLLER v8.0")
        print("===============================")


        for name in self.loader.status()["loaded_engines"]:
result = engine.execute(
    self.pipeline.runner.context
)

self.pipeline.runner.update(
    name,
    result
)

print()
print(name.upper())
print(result)
            engine = self.loader.get(name)

            result = engine.execute(
                self.pipeline.runner.context
            )


            print()
            print(name.upper())
            print(result)



        print()
        print("===============================")
        print("GSIS PIPELINE COMPLETE")
        print("===============================")



if __name__ == "__main__":

    controller = GSISMasterControllerV8()

    controller.run()
