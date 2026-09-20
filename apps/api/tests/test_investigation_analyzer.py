from api.investigation.analyzer import analyze_evidence
from api.investigation.schemas import EvidenceClassification
from api.schemas.evidence import EvidenceItem
from tests.fixtures.evidence_bundles import (
    clearly_suspicious_bundle,
    contradictory_context_bundle,
    insufficient_evidence_bundle,
    mixed_evidence_bundle,
    policy_without_history_bundle,
)

def test_analyze_evidence_returns_all_evidence_items():
    bundle = clearly_suspicious_bundle()

    analyzed = analyze_evidence(bundle)

    assert len(analyzed) == 3
    assert [item.evidence.source_id for item in analyzed] == [
        "txn-001",
        "case-001",
        "policy-001",
    ]

def test_analyze_evidence_preserves_source_evidence():
    bundle = contradictory_context_bundle()

    analyzed = analyze_evidence(bundle)

    assert [item.evidence for item in analyzed] == (
        bundle.transaction_evidence
        + bundle.historical_case_evidence
        + bundle.policy_evidence
    )

def test_analyze_evidence_handles_missing_evidence_groups():
    bundle = insufficient_evidence_bundle()

    analyzed = analyze_evidence(bundle)

    assert len(analyzed) == 1
    assert analyzed[0].evidence.source_id == "txn-004"


def test_analyze_evidence_handles_policy_without_history():
    bundle = policy_without_history_bundle()

    analyzed = analyze_evidence(bundle)

    assert len(analyzed) == 2
    assert [item.evidence.source_id for item in analyzed] == [
        "txn-005",
        "policy-005",
    ]    

def test_analyze_evidence_handles_mixed_evidence():
    bundle = mixed_evidence_bundle()

    analyzed = analyze_evidence(bundle)

    assert len(analyzed) == 3
    assert [item.evidence.source_id for item in analyzed] == [
        "txn-003",
        "case-003",
        "policy-003",
    ]

def test_analyze_evidence_uses_provided_classifier():
    class AlwaysNeutralClassifier:
        def classify(self, evidence: EvidenceItem) -> EvidenceClassification:
            return EvidenceClassification.NEUTRAL

    bundle = clearly_suspicious_bundle()

    analyzed = analyze_evidence(
        bundle,
        classifier=AlwaysNeutralClassifier(),
    )

    assert all(
        item.classification == EvidenceClassification.NEUTRAL
        for item in analyzed
    )    
