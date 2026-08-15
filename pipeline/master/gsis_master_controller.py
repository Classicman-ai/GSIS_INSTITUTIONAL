from datetime import datetime, timezone

from engines.core.config_loader import ConfigLoader

from engines.data.market_data_engine import MarketDataEngine
from engines.volume.volume_intelligence import VolumeIntelligence
from engines.orderflow.order_flow_engine import OrderFlowEngine
from engines.regime.regime_intelligence_engine import RegimeIntelligenceEngine
from engines.adaptive.adaptive_market_intelligence import AdaptiveMarketIntelligence

from engines.fusion.decision_fusion_engine import DecisionFusionEngine
from engines.signals.signal_generator import SignalGenerator

from engines.risk.risk_engine import RiskEngine
from engines.quality.trade_quality_gate import TradeQualityGate


class GSISMasterController:

    def __init__(self):

        self.config = ConfigLoader()

        self.data = MarketDataEngine()
        self.volume = VolumeIntelligence()
        self.orderflow = OrderFlowEngine()
        self.regime = RegimeIntelligenceEngine()
        self.adaptive = AdaptiveMarketIntelligence()

        self.fusion = DecisionFusionEngine()
        self.signal = SignalGenerator()

        self.risk = RiskEngine()
        self.quality = TradeQualityGate()


    def run(self):

        print("===============================")
        print("GSIS MASTER CONTROLLER v7.0")
        print("===============================")

        config = self.config.load()

        print("\nCONFIG:")
        print(config)


        symbol = config["primary_symbol"]

        print("\nPROCESSING:", symbol)


        market = self.data.run(symbol)

        volume = self.volume.run(symbol)

        flow = self.orderflow.run(symbol)

        regime = self.regime.run(symbol)

        adaptive = self.adaptive.run(
            symbol,
            regime,
            volume,
            flow
        )


        fusion = self.fusion.run(
            symbol,
            market,
            volume,
            flow,
            regime,
            adaptive
        )


        print("\nFUSION:")
        print(fusion)



        signal = self.signal.generate(
            symbol,
            fusion,
            regime
        )


        print("\nSIGNAL:")
        print(signal)



        risk = self.risk.calculate(
            symbol,
            signal
        )


        print("\nRISK:")
        print(risk)



        quality = self.quality.check(
            symbol,
            fusion,
            signal,
            risk
        )


        print("\nQUALITY:")
        print(quality)



        if quality["approval"]:

            print("\n===============================")
            print("GSIS TRADE APPROVED")
            print("===============================")

        else:

            print("\nTRADE BLOCKED BY QUALITY GATE")



        return {
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "market": market,
            "volume": volume,
            "flow": flow,
            "regime": regime,
            "adaptive": adaptive,
            "fusion": fusion,
            "signal": signal,
            "risk": risk,
            "quality": quality
        }



if __name__ == "__main__":

    controller = GSISMasterController()
    controller.run()
