"""
=========================================================
GSIS INSTITUTIONAL

ENGINE MANAGER v4.3

Unified Institutional Intelligence Controller

Integrated:

CORE:
- Data Engine
- Candle Engine
- Validation Engine
- History Engine
- Statistical Engine
- Feature Engine

INTELLIGENCE:
- Intelligence Manager
- Displacement Engine
- Liquidity Sweep Engine
- Market Structure Engine
- Smart Money Fusion Engine
- Context Memory Engine
- MTF Intelligence Engine

DECISION:
- Risk Engine
- Decision Engine

EXECUTION:
- Execution Governor
- Smart Order Router
- Broker Adapter
- Execution Monitoring

SYSTEM:
- Communication Bus
- Monitoring Engine
- Pipeline Controller
- Event Intelligence Bridge

=========================================================
"""


import time
import traceback



# CORE

from data_engine import DataEngine
from candle_engine import CandleEngine
from validation_engine import ValidationEngine
from history_engine import HistoryEngine
from statistical_engine import StatisticalEngine



# INTELLIGENCE

from intelligence.feature_engine import FeatureEngine
from intelligence.intelligence_manager import IntelligenceManager



# SMART MONEY

from intelligence.displacement_engine import DisplacementEngine
from intelligence.liquidity_sweep_engine import LiquiditySweepEngine
from intelligence.market_structure_engine import MarketStructureEngine
from intelligence.smart_money_fusion_engine import SmartMoneyFusionEngine
from intelligence.context_memory_engine import ContextMemoryEngine
from intelligence.mtf_intelligence_engine import MTFIntelligenceEngine



# DECISION

from intelligence.risk_engine import RiskEngine
from intelligence.decision_engine import DecisionEngine



# EXECUTION

from intelligence.execution_governor import ExecutionGovernor
from intelligence.smart_order_router import SmartOrderRouter
from intelligence.broker_adapter_engine import BrokerAdapterEngine
from intelligence.execution_monitoring_engine import ExecutionMonitoringEngine



# SYSTEM

from core.communication_bus import CommunicationBus
from core.monitoring_engine import MonitoringEngine
from core.pipeline_controller import PipelineController
from core.event_bridge import EventIntelligenceBridge





class EngineManager:



    def __init__(self):


        print("==============================")
        print("GSIS ENGINE MANAGER v4.3")
        print("==============================")


        # CORE

        self.data_engine = DataEngine()

        self.candle_engine = CandleEngine()

        self.validation_engine = ValidationEngine()

        self.history_engine = HistoryEngine()

        self.statistical_engine = StatisticalEngine()

        self.feature_engine = FeatureEngine()

        self.intelligence_manager = IntelligenceManager()



        # SMART MONEY

        self.displacement_engine = DisplacementEngine()

        self.liquidity_engine = LiquiditySweepEngine()

        self.market_structure_engine = MarketStructureEngine()

        self.smart_money_engine = SmartMoneyFusionEngine()

        self.context_memory_engine = ContextMemoryEngine()

        self.mtf_engine = MTFIntelligenceEngine()



        # DECISION

        self.risk_engine = RiskEngine()

        self.decision_engine = DecisionEngine()



        # EXECUTION

        self.execution_governor = ExecutionGovernor()

        self.order_router = SmartOrderRouter()

        self.broker_adapter = BrokerAdapterEngine()

        self.execution_monitor = ExecutionMonitoringEngine()



        # SYSTEM

        self.communication_bus = CommunicationBus()

        self.monitoring_engine = MonitoringEngine()


        self.pipeline_controller = PipelineController()


        self.event_bridge = EventIntelligenceBridge(
            self.communication_bus,
            self.pipeline_controller
        )



        self.engines = [

            self.data_engine,
            self.candle_engine,
            self.validation_engine,
            self.history_engine,
            self.statistical_engine,
            self.feature_engine,
            self.intelligence_manager,


            self.displacement_engine,
            self.liquidity_engine,
            self.market_structure_engine,
            self.smart_money_engine,
            self.context_memory_engine,
            self.mtf_engine,


            self.risk_engine,
            self.decision_engine,


            self.execution_governor,
            self.order_router,
            self.broker_adapter,
            self.execution_monitor,


            self.pipeline_controller,
            self.event_bridge,


            self.communication_bus,
            self.monitoring_engine

        ]


        self.running = False





    def initialize(self):


        print("==============================")
        print("GSIS INSTITUTIONAL STARTUP")
        print("==============================")


        for engine in self.engines:


            try:


                if hasattr(engine,"initialize"):

                    engine.initialize()



            except Exception as error:


                print(
                    "ENGINE START ERROR:",
                    engine.__class__.__name__,
                    error
                )


                traceback.print_exc()



        self.setup_monitoring()


        self.running = True



        print("==============================")
        print("ALL GSIS ENGINES ONLINE")
        print("==============================")






    def setup_monitoring(self):


        print("==============================")
        print("GSIS MONITORING SETUP")
        print("==============================")


        for engine in self.engines:


            if engine == self.monitoring_engine:

                continue


            try:


                if hasattr(self.monitoring_engine,"register"):

                    self.monitoring_engine.register(engine)


                elif hasattr(self.monitoring_engine,"subscribe"):

                    self.monitoring_engine.subscribe(engine)


                elif hasattr(self.monitoring_engine,"add_monitor"):

                    self.monitoring_engine.add_monitor(engine)


                elif hasattr(self.monitoring_engine,"monitor"):

                    self.monitoring_engine.monitor(engine)



                print(
                    "MONITORED:",
                    engine.__class__.__name__
                )



            except Exception as error:


                print(
                    "MONITOR SKIPPED:",
                    engine.__class__.__name__,
                    error
                )






    def start(self):


        self.initialize()


        while self.running:


            try:

                time.sleep(5)


            except KeyboardInterrupt:


                self.shutdown()

                break






    def run(self):


        self.start()






    def shutdown(self):


        self.running = False


        print("==============================")
        print("GSIS SYSTEM STOPPED")
        print("==============================")
