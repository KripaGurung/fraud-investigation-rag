from api.investigation.context import build_investigation_context
from api.investigation.generation.prompt import build_investigation_prompt
from tests.fixtures.evidence_bundles import (
    clearly_suspicious_bundle,
    insufficient_evidence_bundle,
)


def test_prompt_contains_alert_id_and_evidence_details() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    prompt = build_investigation_prompt(bundle.alert_id, context)

    assert bundle.alert_id in prompt
    assert "txn-001" in prompt
    assert "case-001" in prompt
    assert "policy-001" in prompt
    assert (
    "Transaction amount is significantly above the customer's usual range."
    in prompt
    )


def test_prompt_contains_missing_evidence() -> None:
    bundle = insufficient_evidence_bundle()
    context = build_investigation_context(bundle)

    prompt = build_investigation_prompt(bundle.alert_id, context)

    assert "historical_case_evidence" in prompt
    assert "policy_evidence" in prompt


def test_prompt_requires_grounded_generation() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    prompt = build_investigation_prompt(bundle.alert_id, context)

    assert "Use only the evidence provided below." in prompt
    assert "Do not invent evidence, facts, or evidence IDs." in prompt
    assert (
        "Every generated finding must reference only Evidence IDs listed below."
        in prompt
    )