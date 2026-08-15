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

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, CORE_DIR)


from gsis_master_intelligence_adapter import (
    GSISMasterIntelligenceAdapter
)

from risk_position_engine import RiskPositionEngine
from decision_governor_engine import DecisionGovernorEngine

from trade_lifecycle_engine import TradeLifecycleEngine
from execution_control_engine import ExecutionControlEngine
from broker_execution_gate import BrokerExecutionGate

from trade_monitor_engine import TradeMonitorEngine
from trade_management_engine import TradeManagementEngine

from trade_audit_engine import TradeAuditEngine

from signal_memory_engine import SignalMemoryEngine
from auto_learning_loop import AutoLearningLoop

from system_health_monitor_engine import SystemHealthMonitorEngine
from configuration_control_engine import ConfigurationControlEngine
from recovery_control_engine import RecoveryControlEngine
from pipeline_telemetry_engine import PipelineTelemetryEngine



class GSISMasterOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER ORCHESTRATOR v4.2 ONLINE")
        print("ADAPTIVE INSTITUTIONAL PIPELINE ACTIVE")
        print("==============================")


        self.config = ConfigurationControlEngine()

        self.health = SystemHealthMonitorEngine()

        self.recovery = RecoveryControlEngine()

        self.telemetry = PipelineTelemetryEngine()


        self.intelligence = GSISMasterIntelligenceAdapter()


        self.risk = RiskPositionEngine()

        self.decision = DecisionGovernorEngine()


        self.lifecycle = TradeLifecycleEngine()

        self.execution = ExecutionControlEngine()

        self.broker = BrokerExecutionGate()


        self.monitor = TradeMonitorEngine()

        self.management = TradeManagementEngine()

        self.audit = TradeAuditEngine()


        self.memory = SignalMemoryEngine()

        self.learning = AutoLearningLoop()



    def execute_method(
        self,
        engine,
        methods,
        argument
    ):

        for method in methods:

            if hasattr(engine, method):

                return getattr(
                    engine,
                    method
                )(argument)


        return {

            "status":
            "METHOD NOT FOUND",

            "engine":
            engine.__class__.__name__

        }



    def run_pipeline(
        self,
        signal,
        context
    ):


        print("==============================")
        print("GSIS PIPELINE START")
        print("==============================")


        health = self.health.check(

            engines_loaded=True,

            market_feed=True,

            memory_system=True,

            execution_system=True

        )


        print(health)



        intelligence = self.intelligence.analyze(

            context

        )


        fusion = intelligence.get(
            "decision",
            {}
        )


        print("INTELLIGENCE")
        print(intelligence)



        risk = self.risk.calculate_position(

            signal

        )


        print("RISK")
        print(risk)



        governor = self.decision.evaluate(

            {

                "confidence":
                fusion.get(
                    "confidence",
                    0
                ),

                "pattern_match":
                fusion.get(
                    "confidence",
                    0
                )

            },

            risk,

            {

                "liquidity_state":
                "ACTIVE",

                "volatility":
                "NORMAL"

            }

        )


        print("GOVERNOR")
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

            fusion.get(
                "decision_direction",
                signal["direction"]
            ),

            signal["entry"],

            signal["stop_loss"],

            signal["tp1"],

            fusion.get(
                "confidence",
                0
            ),

            fusion.get(
                "reasons",
                []
            )

        )


        print("TRADE")
        print(trade)



        execution = self.execute_method(

            self.execution,

            [

                "authorize_execution",

                "authorize_trade"

            ],

            trade

        )


        print("EXECUTION")
        print(execution)



        broker = self.execute_method(

            self.broker,

            [

                "execute_order",

                "execute_trade"

            ],

            execution

        )


        print("BROKER")
        print(broker)



        monitor = self.execute_method(

            self.monitor,

            [

                "monitor_trade",

                "monitor"

            ],

            trade

        )


        management = self.execute_method(

            self.management,

            [

                "manage_trade",

                "manage"

            ],

            trade

        )



        audit = self.audit.record(

            trade["trade_id"],

            governor.get(
                "decision",
                "UNKNOWN"
            ),

            execution.get(
                "status",
                "UNKNOWN"
            ),

            broker.get(
                "broker_status",
                broker.get(
                    "status",
                    "UNKNOWN"
                )
            ),

            "VALIDATED"

        )


        self.memory.store_signal(
            signal
        )

        self.learning.learn(
            signal
        )


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

        "tp1":2395

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
        {},

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
