from datetime import datetime


class TradeSetupEngine:

    def __init__(self):
        print("==============================")
        print("GSIS TRADE SETUP ENGINE v1.1 ONLINE")
        print("==============================")
        print("INSTITUTIONAL TRADE PLANNING ACTIVE")
        print("==============================")


    def generate(self, risk_data):

        if risk_data is None:
            return None


        symbol = risk_data.get(
            "symbol",
            "XAUUSD"
        )

        decision = risk_data.get(
            "decision",
            "WAIT"
        )

        status = risk_data.get(
            "status",
            "BLOCKED"
        )


        if decision == "BUY" and status == "APPROVED":

            setup = {

                "symbol": symbol,
                "setup_status": "APPROVED",
                "direction": "BUY",
                "entry_type": "MARKET",
                "risk_status": status,
                "timestamp": datetime.utcnow().isoformat()

            }


        elif decision == "SELL" and status == "APPROVED":

            setup = {

                "symbol": symbol,
                "setup_status": "APPROVED",
                "direction": "SELL",
                "entry_type": "MARKET",
                "risk_status": status,
                "timestamp": datetime.utcnow().isoformat()

            }


        else:

            setup = {

                "symbol": symbol,
                "setup_status": "REJECTED",
                "reason": "Risk control has not approved trade",
                "decision": decision,
                "timestamp": datetime.utcnow().isoformat()

            }


        print("==============================")
        print("GSIS TRADE SETUP ANALYSIS")
        print("==============================")

        print("RISK INPUT:")
        print(risk_data)

        print()

        print("TRADE SETUP RESULT:")
        print(setup)


        return setup



engine = TradeSetupEngine()
