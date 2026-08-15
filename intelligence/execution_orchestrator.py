"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION ORCHESTRATOR

Version: 6.0

Institutional Pipeline Controller

=========================================================
"""

from datetime import datetime
import uuid

from intelligence.execution_context import ExecutionContext


class ExecutionOrchestrator:

    def __init__(self):

        self.name = "Execution Orchestrator"

        self.status = "CREATED"

        self.engines = []

        self.history = []



    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EXECUTION ORCHESTRATOR ONLINE")
        print("==============================")


    def register_engine(self, engine):

        self.engines.append(engine)

        print(
            f"REGISTERED: {engine.__class__.__name__}"
        )


    def process(
            self,
            asset,
            signal,
            price):


        context = ExecutionContext()

        context.asset = asset

        context.signal = signal

        context.price = price

        context.timestamp = str(datetime.utcnow())

        context.log(
            "ORCHESTRATOR",
            "Execution Started"
        )


        for engine in self.engines:

            try:

                context = engine.process(context)

            except Exception as error:

                context.log(

                    engine.__class__.__name__,

                    str(error)

                )

                context.decision = "FAILED"

                context.approved = False

                break


        report = {

            "execution_id":

            str(uuid.uuid4()),

            "timestamp":

            str(datetime.utcnow()),

            "summary":

            context.summary()

        }

        self.history.append(report)

        return context


    def report(self):

        return self.history
