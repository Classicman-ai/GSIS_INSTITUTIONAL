"""
=========================================================
GSIS INSTITUTIONAL

EXECUTION COMPLIANCE &
AUDIT INTELLIGENCE ENGINE (IECAIE)

Version: 1.0

Functions:
- Validate execution compliance
- Record audit trail
- Explain execution decisions

=========================================================
"""

from datetime import datetime
import uuid


class ExecutionComplianceEngine:

    def __init__(self):

        self.name = "Execution Compliance & Audit Intelligence Engine"

        self.status = "CREATED"

        self.audit_log = []


    def initialize(self):

        self.status = "ONLINE"

        print("==============================")
        print("EXECUTION COMPLIANCE ENGINE ONLINE")
        print("==============================")


    def validate(
            self,
            asset,
            signal,
            risk_score,
            liquidity_score,
            execution_mode,
            approved):


        compliance = (
            approved
            and
            risk_score < 70
            and
            liquidity_score >= 50
        )


        record = {

            "audit_id":
            str(uuid.uuid4()),

            "timestamp":
            str(datetime.utcnow()),

            "asset":
            asset,

            "signal":
            signal,

            "risk_score":
            risk_score,

            "liquidity_score":
            liquidity_score,

            "execution_mode":
            execution_mode,

            "approved":
            approved,

            "compliance":
            compliance,

            "status":
            "RECORDED"

        }


        self.audit_log.append(
            record
        )


        return record


    def history(self):

        return self.audit_log


    def latest(self):

        if not self.audit_log:

            return None

        return self.audit_log[-1]
