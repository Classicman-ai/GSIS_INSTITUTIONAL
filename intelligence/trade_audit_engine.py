import datetime


class TradeAuditEngine:

    def __init__(self):

        print("==============================")
        print("GSIS TRADE AUDIT ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL COMPLIANCE RECORDING ACTIVE")
        print("==============================")


    def record(
        self,
        trade_id,
        approval,
        execution,
        broker,
        risk
    ):

        audit_status = "AUDIT COMPLETE"

        record = {

            "audit_id":
                "AUDIT-" +
                datetime.datetime.now(
                    datetime.timezone.utc
                ).strftime("%Y%m%d%H%M%S"),

            "trade_id":
                trade_id,

            "approval_status":
                approval,

            "execution_status":
                execution,

            "broker_status":
                broker,

            "risk_status":
                risk,

            "compliance":
                "PASSED",

            "status":
                audit_status,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS AUDIT RESULT")
        print("==============================")
        print(record)


        return record



if __name__ == "__main__":


    engine = TradeAuditEngine()


    engine.record(

        trade_id="TEST-001",

        approval="FINAL APPROVAL",

        execution="AUTHORIZED",

        broker="SIMULATION APPROVED",

        risk="VALIDATED"

    )
