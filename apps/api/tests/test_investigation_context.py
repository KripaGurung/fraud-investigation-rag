from api.investigation.context import build_investigation_context
from api.investigation.schemas import EvidenceClassification
from api.schemas.evidence import EvidenceItem
from tests.fixtures.evidence_bundles import (
    clearly_suspicious_bundle,
    insufficient_evidence_bundle,
)


def test_build_investigation_context_contains_analyzed_evidence():
    bundle = clearly_suspicious_bundle()

    context = build_investigation_context(bundle)

    assert len(context.analyzed_evidence) == 3
    assert [item.evidence.source_id for item in context.analyzed_evidence] == [
        "txn-001",
        "case-001",
        "policy-001",
    ]

def test_build_investigation_context_contains_missing_evidence():
    bundle = insufficient_evidence_bundle()

    context = build_investigation_context(bundle)

    assert "historical_case_evidence" in context.missing_evidence
    assert "policy_evidence" in context.missing_evidence    

def test_build_investigation_context_has_no_missing_evidence_when_complete():
    bundle = clearly_suspicious_bundle()

    context = build_investigation_context(bundle)

    assert context.missing_evidence == []

def test_build_investigation_context_uses_provided_classifier():
    class AlwaysNeutralClassifier:
        def classify(self, evidence: EvidenceItem) -> EvidenceClassification:
            return EvidenceClassification.NEUTRAL

    bundle = clearly_suspicious_bundle()

    context = build_investigation_context(
        bundle,
        classifier=AlwaysNeutralClassifier(),
    )

    assert all(
        item.classification == EvidenceClassification.NEUTRAL
        for item in context.analyzed_evidence
    )

def test_build_investigation_context_preserves_evidence_order():
    bundle = clearly_suspicious_bundle()

    context = build_investigation_context(bundle)

    assert [item.evidence.source_id for item in context.analyzed_evidence] == [
        "txn-001",
        "case-001",
        "policy-001",
    ]            