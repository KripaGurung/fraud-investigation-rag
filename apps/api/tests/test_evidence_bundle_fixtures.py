from api.schemas.evidence import EvidenceBundle
from tests.fixtures.evidence_bundles import (
    clearly_suspicious_bundle,
    contradictory_context_bundle,
    insufficient_evidence_bundle,
    mixed_evidence_bundle,
    policy_without_history_bundle,
)

def test_clearly_suspicious_bundle_has_expected_evidence():
    bundle = clearly_suspicious_bundle()

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "alert-suspicious-001"
    assert len(bundle.transaction_evidence) == 1
    assert len(bundle.historical_case_evidence) == 1
    assert len(bundle.policy_evidence) == 1


def test_contradictory_context_bundle_has_expected_evidence():
    bundle = contradictory_context_bundle()

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "alert-contradictory-001"
    assert len(bundle.transaction_evidence) == 1
    assert len(bundle.historical_case_evidence) == 1
    assert len(bundle.policy_evidence) == 1  


def test_mixed_evidence_bundle_has_expected_evidence():
    bundle = mixed_evidence_bundle()

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "alert-mixed-001"
    assert len(bundle.transaction_evidence) == 1
    assert len(bundle.historical_case_evidence) == 1
    assert len(bundle.policy_evidence) == 1      


def test_insufficient_evidence_bundle_has_expected_gaps():
    bundle = insufficient_evidence_bundle()

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "alert-insufficient-001"
    assert len(bundle.transaction_evidence) == 1
    assert bundle.historical_case_evidence == []
    assert bundle.policy_evidence == []


def test_policy_without_history_bundle_has_expected_gap():
    bundle = policy_without_history_bundle()

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "alert-policy-no-history-001"
    assert len(bundle.transaction_evidence) == 1
    assert bundle.historical_case_evidence == []
    assert len(bundle.policy_evidence) == 1

    