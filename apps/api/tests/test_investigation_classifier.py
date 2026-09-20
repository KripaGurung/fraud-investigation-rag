import pytest

from api.investigation.classifier import (
    DeterministicEvidenceClassifier,
    EvidenceClassifier,
)
from api.investigation.schemas import EvidenceClassification
from api.schemas.evidence import EvidenceItem

@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("This transaction is suspicious.", EvidenceClassification.SUPPORTING),
        ("The transaction is unusually large.", EvidenceClassification.SUPPORTING),
        (
            "Similar transactions were confirmed as legitimate.",
            EvidenceClassification.CONTRADICTING,
        ),
        (
            "The customer previously made legitimate business payments.",
            EvidenceClassification.CONTRADICTING,
        ),
        (
            "The transaction amount was 5000 USD.",
            EvidenceClassification.NEUTRAL,
        ),
        (
            "The transaction is suspicious but was previously confirmed as legitimate.",
            EvidenceClassification.NEUTRAL,
        ),
        (
            "High-value payments to new beneficiaries require additional review.",
            EvidenceClassification.SUPPORTING,
        ),
        (
            "The customer has previously made legitimate high-value payments to new beneficiaries.",
            EvidenceClassification.CONTRADICTING,
        ),
    ],
)
def test_deterministic_classifier_rules(
    content: str,
    expected: EvidenceClassification,
):
    classifier = DeterministicEvidenceClassifier()
    evidence = EvidenceItem(
        source_id="test-rule",
        source_type="transaction",
        content=content,
        score=0.90,
    )

    assert classifier.classify(evidence) == expected

class StubEvidenceClassifier:
    def classify(self, evidence: EvidenceItem) -> EvidenceClassification:
        return EvidenceClassification.NEUTRAL


def test_classifier_implementation_satisfies_protocol():
    classifier = StubEvidenceClassifier()

    assert isinstance(classifier, EvidenceClassifier)

def test_deterministic_classifier_classifies_suspicious_evidence():
    classifier = DeterministicEvidenceClassifier()
    evidence = EvidenceItem(
        source_id="test-001",
        source_type="transaction",
        content="This transaction is suspicious.",
        score=0.90,
    )

    result = classifier.classify(evidence)

    assert result == EvidenceClassification.SUPPORTING

def test_deterministic_classifier_classifies_legitimate_evidence():
    classifier = DeterministicEvidenceClassifier()
    evidence = EvidenceItem(
        source_id="test-002",
        source_type="historical_case",
        content="Similar transactions were confirmed as legitimate.",
        score=0.90,
    )

    result = classifier.classify(evidence)

    assert result == EvidenceClassification.CONTRADICTING

def test_deterministic_classifier_classifies_neutral_evidence():
    classifier = DeterministicEvidenceClassifier()
    evidence = EvidenceItem(
        source_id="test-003",
        source_type="transaction",
        content="The transaction amount was 5000 USD.",
        score=0.90,
    )

    result = classifier.classify(evidence)

    assert result == EvidenceClassification.NEUTRAL
        