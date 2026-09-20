from api.investigation.gaps import detect_missing_evidence
from api.schemas.evidence import EvidenceBundle, EvidenceItem
from tests.fixtures.evidence_bundles import (
    clearly_suspicious_bundle,
    insufficient_evidence_bundle,
    policy_without_history_bundle,
)

def test_detects_missing_history_and_policy_evidence():
    bundle = insufficient_evidence_bundle()

    missing = detect_missing_evidence(bundle)

    assert "historical_case_evidence" in missing
    assert "policy_evidence" in missing

def test_detects_missing_history_when_policy_is_present():
    bundle = policy_without_history_bundle()

    missing = detect_missing_evidence(bundle)

    assert "historical_case_evidence" in missing
    assert "policy_evidence" not in missing  

def test_detects_missing_policy_when_history_is_present():
    bundle = EvidenceBundle(
        alert_id="alert-gap-test",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-gap",
                source_type="transaction",
                content="A transaction triggered an alert.",
                score=0.90,
            )
        ],
        historical_case_evidence=[
            EvidenceItem(
                source_id="case-gap",
                source_type="historical_case",
                content="A similar historical case was reviewed.",
                score=0.80,
            )
        ],
        policy_evidence=[],
    )

    missing = detect_missing_evidence(bundle)

    assert "historical_case_evidence" not in missing
    assert "policy_evidence" in missing

def test_detects_missing_transaction_evidence():
    bundle = EvidenceBundle(
        alert_id="alert-no-transaction",
        transaction_evidence=[],
        historical_case_evidence=[],
        policy_evidence=[],
    )

    missing = detect_missing_evidence(bundle)

    assert "transaction_evidence" in missing

def test_returns_no_missing_evidence_when_all_categories_are_present():
    bundle = clearly_suspicious_bundle()

    missing = detect_missing_evidence(bundle)

    assert missing == []              