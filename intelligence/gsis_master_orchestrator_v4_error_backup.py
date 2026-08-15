import datetime
import sys
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CORE_DIR = os.path.join(
    BASE_DIR,
    "core"
)

sys.path.append(BASE_DIR)
sys.path.append(CORE_DIR)


from intelligence_bridge import IntelligenceBridge
from auto_learning_loop import AutoLearningLoop
from signal_memory_engine import SignalMemoryEngine

from risk_position_engine import RiskPositionEngine
from decision_governor_engine import DecisionGovernorEngine
from portfolio_risk_governor_engine import PortfolioRiskGovernorEngine

from trade_lifecycle_engine import TradeLifecycleEngine
from execution_control_engine import ExecutionControlEngine
from broker_execution_gate import BrokerExecutionGate

from trade_monitor_engine import TradeMonitorEngine
from trade_management_engine import TradeManagementEngine

from trade_audit_engine import TradeAuditEngine

from system_health_monitor_engine import SystemHealthMonitorEngine
from recovery_control_engine import RecoveryControlEngine
from configuration_control_engine import ConfigurationControlEngine
from pipeline_telemetry_engine import PipelineTelemetryEngine


from gsis_master_intelligence_adapter import (
    GSISMasterIntelligenceAdapter
)



class GSISMasterOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER ORCHESTRATOR v4.0 ONLINE")
        print("FULL INTELLIGENCE + EXECUTION PIPELINE ACTIVE")
        print("==============================")


        self.config = ConfigurationControlEngine()

        self.health = SystemHealthMonitorEngine()

        self.recovery = RecoveryControlEngine()

        self.telemetry = PipelineTelemetryEngine()


        # New intelligence brain

        self.master_intelligence = (
            GSISMasterIntelligenceAdapter()
        )


        # Existing execution intelligence

        self.intelligence = IntelligenceBridge()

        self.learning = AutoLearningLoop()

        self.memory = SignalMemoryEngine()


        self.risk = RiskPositionEngine()

        self.decision = DecisionGovernorEngine()

        self.portfolio = PortfolioRiskGovernorEngine()


        self.lifecycle = TradeLifecycleEngine()

        self.execution = ExecutionControlEngine()

        self.broker = BrokerExecutionGate()


        self.monitor = TradeMonitorEngine()

        self.management = TradeManagementEngine()

        self.audit = TradeAuditEngine()



    def run_pipeline(self, signal, context):


        print("==============================")
        print("GSIS MASTER PIPELINE START")
        print("==============================")


        health = self.health.check(

            engines_loaded=True,

            market_feed=True,

            memory_system=True,

            execution_system=True

        )


        print("HEALTH RESULT")
        print(health)



        intelligence = self.master_intelligence.analyze(

            context

        )


        print("MASTER INTELLIGENCE RESULT")
        print(intelligence)



        decision_data = intelligence.get(
            "decision",
            {}
        )


        confidence = decision_data.get(
            "confidence",
            0
        )



        governor = self.decision.evaluate(

            confidence=confidence,

            pattern_score=confidence,

            risk_valid=True

        )


        print("GOVERNOR RESULT")
        print(governor)



        if governor.get("decision") != "APPROVED":


            return {

                "status":
                "TRADE REJECTED",

                "reason":
                governor

            }



        trade = self.lifecycle.open_trade(

            signal["symbol"],

            decision_data.get(
                "decision_direction",
                signal["direction"]
            ),

            signal["entry"],

            signal["stop_loss"],

            signal["tp1"],

            confidence,

            decision_data.get(
                "reasons",
                []
            )

        )


        print("TRADE RESULT")
        print(trade)



        execution = self.execution.authorize_trade(

            trade

        )


        print("EXECUTION RESULT")
        print(execution)



        broker = self.broker.execute_order(

            execution

        )


        print("BROKER RESULT")
        print(broker)



        monitor = self.monitor.monitor_trade(

            trade

        )


        management = self.management.manage_trade(

            trade

        )


        audit = self.audit.record(

            trade["trade_id"],

            governor["decision"],

            execution["status"],

            broker["broker_status"],

            "VALIDATED"

        )


        self.learning.learn(signal)

        self.memory.store_signal(signal)



        result = {


            "status":

            "PIPELINE COMPLETE",


            "intelligence":

            intelligence,


            "trade":

            trade,


            "execution":

            execution,


            "broker":

            broker,


            "monitor":

            monitor,


            "management":

            management,


            "audit":

            audit,


            "timestamp":

            datetime.datetime.now(

                datetime.timezone.utc

            ).isoformat()


        }


        print("==============================")
        print("GSIS MASTER RESULT")
        print("==============================")

        print(result)


        return result




if __name__ == "__main__":


    engine = GSISMasterOrchestrator()


    signal = {

        "symbol":"XAUUSD",

        "direction":"BUY",

        "entry":2389.5,

        "stop_loss":2386.5,

        "tp1":2395,

        "confidence":80,

        "reasons":[]

    }


    context = {


        "structure":

        {

            "trend":"BULLISH",

            "bos":True

        },


        "zone":

        {

            "nearest_zone":"DEMAND"

        },


        "liquidity":

        {

            "liquidity_sweeps":

            [

                "SELL_SIDE_SWEEP"

            ]

        },


        "candlestick":

        {

            "patterns":

            [

                "BULLISH_ENGULFING"

            ]

        },


        "chart_pattern":

        {

            "patterns":[]

        },


        "economic":

        {

            "high_impact":0

        },


        "pattern":

        "BULLISH_ENGULFING"

    }


    engine.run_pipeline(

        signal,

        context

    )
