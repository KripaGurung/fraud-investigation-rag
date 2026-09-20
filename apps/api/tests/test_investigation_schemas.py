import pytest
from pydantic import ValidationError

from api.investigation.schemas import AnalyzedEvidence, EvidenceClassification
from api.schemas.evidence import EvidenceItem


def test_analyzed_evidence_preserves_original_evidence():
    evidence = EvidenceItem(
        source_id="txn-001",
        source_type="transaction",
        content="Transaction amount is significantly above the customer's usual range.",
        score=0.95,
        metadata={"transaction_id": "txn-001"},
    )

    analyzed = AnalyzedEvidence(
        evidence=evidence,
        classification=EvidenceClassification.SUPPORTING,
        explanation="The transaction deviates significantly from the customer's usual behavior.",
    )

    assert analyzed.evidence == evidence
    assert analyzed.classification == EvidenceClassification.SUPPORTING
    assert analyzed.explanation == (
        "The transaction deviates significantly from the customer's usual behavior."
    )


def test_analyzed_evidence_rejects_invalid_classification():
    evidence = EvidenceItem(
        source_id="txn-002",
        source_type="transaction",
        content="Transaction evidence.",
        score=0.80,
    )

    with pytest.raises(ValidationError):
        AnalyzedEvidence(
            evidence=evidence,
            classification="suspicious",
            explanation="Invalid classification should not be accepted.",
        )
        