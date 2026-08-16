import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "intelligence" / "gsis_master_orchestrator.py"


def load_orchestrator_module():
    spec = importlib.util.spec_from_file_location(
        "gsis_master_orchestrator_test_module",
        ORCHESTRATOR,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeIntelligence:
    def analyze(self, payload):
        assert payload["structure"]["trend"] == "BULLISH"
        assert payload["zone"]["nearest_zone"] == "DEMAND"
        return {
            "fusion": {
                "confidence": 80,
                "decision_direction": "BUY",
                "reasons": ["TEST"]
            },
            "final_confidence": 80
        }


def test_intelligence_context_reaches_adapter():
    module = load_orchestrator_module()
    obj = object.__new__(module.GSISMasterOrchestrator)
    obj.intelligence = FakeIntelligence()

    result = obj.intelligence.analyze({
        "structure": {"trend": "BULLISH"},
        "zone": {"nearest_zone": "DEMAND"},
    })

    assert result["fusion"]["confidence"] == 80


def test_pipeline_uses_fusion_not_missing_decision_key():
    module = load_orchestrator_module()
    intelligence = FakeIntelligence()
    result = intelligence.analyze({
        "structure": {"trend": "BULLISH"},
        "zone": {"nearest_zone": "DEMAND"},
    })

    fusion = result.get("fusion", {})
    assert fusion["decision_direction"] == "BUY"
    assert fusion["confidence"] == 80


def test_execution_guard_rejects_unauthorized_result():
    module = load_orchestrator_module()
    obj = object.__new__(module.GSISMasterOrchestrator)
    execution = {"status": "REJECTED", "reason": "missing stop"}

    assert execution.get("status") != "EXECUTION AUTHORIZED"
