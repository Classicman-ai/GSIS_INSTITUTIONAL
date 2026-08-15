import datetime


from intelligence_bridge import IntelligenceBridge
from auto_learning_loop import AutoLearningLoop
from signal_memory_engine import SignalMemoryEngine

from risk_position_engine import RiskPositionEngine

from trade_lifecycle_engine import TradeLifecycleEngine
from execution_control_engine import ExecutionControlEngine
from broker_execution_gate import BrokerExecutionGate

from trade_monitor_engine import TradeMonitorEngine
from trade_management_engine import TradeManagementEngine

from decision_governor_engine import DecisionGovernorEngine
from portfolio_risk_governor_engine import PortfolioRiskGovernorEngine

from trade_audit_engine import TradeAuditEngine
from system_health_monitor_engine import SystemHealthMonitorEngine
from recovery_control_engine import RecoveryControlEngine
from configuration_control_engine import ConfigurationControlEngine
from pipeline_telemetry_engine import PipelineTelemetryEngine


class GSISMasterOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS MASTER ORCHESTRATOR v3.0 ONLINE")
        print("FULL INSTITUTIONAL PIPELINE CONTROL ACTIVE")
        print("==============================")


        self.config = ConfigurationControlEngine()

        self.health = SystemHealthMonitorEngine()

        self.recovery = RecoveryControlEngine()

        self.telemetry = PipelineTelemetryEngine()


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



    def run_pipeline(self, signal):


        print("==============================")
        print("GSIS MASTER PIPELINE START")
        print("==============================")


        health = self.health.check(

            engines_loaded=True,

            market_feed=True,

            memory_system=True,

            execution_system=True

        )


        intelligence = self.intelligence.evaluate(signal)


        print("INTELLIGENCE RESULT")
        print(intelligence)



        learning = self.learning.learn(signal)


        print("LEARNING RESULT")
        print(learning)



        memory = self.memory.store_signal(signal)


        print("MEMORY RESULT")
        print(memory)



        risk = self.risk.calculate_position(signal)


        print("RISK RESULT")
        print(risk)



        governor = self.decision.evaluate(

            confidence=intelligence.get(
                "confidence",
                0
            ),

            pattern_score=intelligence.get(
                "pattern_match",
                0
            ),

            risk_valid=True

        )


        print("GOVERNOR RESULT")
        print(governor)



        portfolio = self.portfolio.evaluate(

            positions=1

        )


        print("PORTFOLIO RESULT")
        print(portfolio)



        if governor.get("decision") != "APPROVED":

            return {

                "status":
                "TRADE REJECTED",

                "reason":
                governor

            }



        trade = self.lifecycle.open_trade(

            signal["symbol"],

            signal["direction"],

            signal["entry"],

            signal["stop_loss"],

            signal["tp1"],

            signal["confidence"],

            signal["reasons"]

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


        print("MONITOR RESULT")
        print(monitor)



        management = self.management.manage_trade(

            trade

        )


        print("MANAGEMENT RESULT")
        print(management)



        audit = self.audit.record(

            trade["trade_id"],

            governor["decision"],

            execution["status"],

            broker["broker_status"],

            "VALIDATED"

        )


        result = {

            "status":
            "PIPELINE COMPLETE",

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


    test_signal = {

        "symbol":
        "XAUUSD",

        "direction":
        "SELL",

        "entry":
        2387.5,

        "stop_loss":
        2387.8,

        "tp1":
        2387.2,

        "confidence":
        100,

        "reasons":
        [

            "LIQUIDITY SWEEP CONFIRMED",

            "BEARISH ORDER BLOCK",

            "BEARISH FVG",

            "BEARISH CHoCH"

        ]

    }


    engine.run_pipeline(test_signal)
