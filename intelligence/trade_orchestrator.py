from intelligence.execution_control_engine import ExecutionControlEngine
from intelligence.risk_management_engine import RiskManagementEngine
from intelligence.position_sizing_engine import PositionSizingEngine
from intelligence.trade_planner_engine import TradePlannerEngine



class TradeOrchestrator:


    def __init__(self):

        print("==============================")
        print("GSIS TRADE ORCHESTRATOR v1.5 ONLINE")
        print("==============================")
        print("INSTITUTIONAL EXECUTION PIPELINE ACTIVE")
        print("==============================")


        self.planner = TradePlannerEngine()

        self.position_engine = PositionSizingEngine()

        self.risk_engine = RiskManagementEngine()

        self.execution_engine = ExecutionControlEngine()



    def process(
        self,
        validation_result,
        balance=100000,
        risk_percent=0.5
    ):


        print("==============================")
        print("GSIS ORCHESTRATOR START")
        print("==============================")


        if validation_result.get("status") != "APPROVED":

            return {

                "status": "REJECTED",

                "reason": "VALIDATION FAILED"

            }



        # ==============================
        # SMART MONEY DATA BRIDGE
        # ==============================


        order_block = validation_result.get(

            "order_block",

            {

                "type": "BEARISH",

                "high": 2387.60,

                "low": 2386.90,

                "status": "ACTIVE"

            }

        )



        fvg = validation_result.get(

            "fvg",

            {

                "type": "BEARISH",

                "gap_high": 2387.50,

                "gap_low": 2386.70,

                "status": "ACTIVE"

            }

        )



        # ==============================
        # TRADE PLANNER
        # ==============================


        trade_plan = self.planner.plan(

            validation_result,

            order_block,

            fvg

        )


        print("==============================")
        print("TRADE PLAN")
        print("==============================")

        print(trade_plan)



        # ==============================
        # POSITION SIZING
        # ==============================


        position = self.position_engine.calculate(

            symbol=trade_plan["symbol"],

            balance=balance,

            risk_percent=risk_percent,

            entry=trade_plan["entry"],

            stop_loss=trade_plan["stop_loss"]

        )


        print("==============================")
        print("POSITION RESULT")
        print("==============================")

        print(position)



        # ==============================
        # RISK CONTROL
        # ==============================


        risk = self.risk_engine.evaluate(

            {

                "symbol": position["symbol"],

                "lot_size": position.get(

                    "approved_lot",

                    position.get("lot_size", 0)

                ),

                "risk_amount": position["risk_amount"],

                "risk_percent": position["risk_percent"]

            }

        )



        print("==============================")
        print("RISK RESULT")
        print("==============================")

        print(risk)



        # ==============================
        # EXECUTION BRIDGE
        # ==============================


        execution_position = position.copy()


        execution_position["lot_size"] = position.get(

            "approved_lot",

            position.get("lot_size", 0)

        )



        execution = self.execution_engine.validate_execution(

            trade_plan,

            risk,

            execution_position

        )


        print("==============================")
        print("EXECUTION RESULT")
        print("==============================")

        print(execution)



        final_result = {


            "trade_plan": trade_plan,

            "position": position,

            "risk": risk,

            "execution": execution

        }



        print("==============================")
        print("GSIS FINAL ORCHESTRATION RESULT")
        print("==============================")


        print(final_result)



        return final_result



if __name__ == "__main__":


    engine = TradeOrchestrator()


    test_validation = {


        "symbol": "XAUUSD",

        "setup": "VALID",

        "direction": "SELL",

        "confidence": 100,

        "status": "APPROVED"


    }


    engine.process(

        test_validation,

        balance=100000,

        risk_percent=0.5

    )
