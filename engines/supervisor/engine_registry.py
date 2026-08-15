# ==========================================
# GSIS ENGINE REGISTRY v3.0
# ==========================================

ENGINES = {

    "HMM": {
        "file": "data/live/HMM_state.json",
        "timeout": 90
    },

    "ORDERFLOW": {
        "file": "data/live/ORDERFLOW_state.json",
        "timeout": 90
    },

    "STRUCTURE": {
        "file": "data/live/STRUCTURE_state.json",
        "timeout": 90
    },

    "FUSION": {
        "file": "data/live/FUSION_state.json",
        "timeout": 90
    },

    "DECISION": {
        "file": "data/live/DECISION_state.json",
        "timeout": 90
    },

    "CONFIRMATION": {
        "file": "data/live/CONFIRMATION_state.json",
        "timeout": 120
    },

    "QUALIFICATION": {
        "file": "data/live/QUALIFICATION_state.json",
        "timeout": 120
    },

    "RISK": {
        "file": "data/live/RISK_state.json",
        "timeout": 120
    },

    "EXECUTION": {
        "file": "data/live/EXECUTION_state.json",
        "timeout": 120
    },

    "REPORT": {
        "file": "data/live/REPORT_state.json",
        "timeout": 120
    },

    "DATABASE": {
        "file": "data/live/database.json",
        "timeout": 180
    },

    "ALERT": {
        "file": "data/live/alert_state.json",
        "timeout": 180
    }
}


def get_engines():
    return ENGINES
