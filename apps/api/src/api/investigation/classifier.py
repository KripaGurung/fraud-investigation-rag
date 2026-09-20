from typing import Protocol, runtime_checkable

from api.investigation.schemas import EvidenceClassification
from api.schemas.evidence import EvidenceItem


SUPPORTING_INDICATORS = (
    "fraud",
    "suspicious",
    "unusual",
    "outside",
    "requires investigation",
    "requires review",
    "require additional review",
    "new beneficiary",
    "new beneficiaries",
    "not previously",
)

CONTRADICTING_INDICATORS = (
    "legitimate",
    "confirmed as legitimate",
    "previously reviewed",
    "previously made legitimate",
)

HISTORICAL_LEGITIMATE_INDICATORS = (
    "previously made legitimate",
    "has previously made legitimate",
)


@runtime_checkable
class EvidenceClassifier(Protocol):
    """Contract for evidence classification implementations."""

    def classify(self, evidence: EvidenceItem) -> EvidenceClassification:
        """Classify a single evidence item."""
        ...


class DeterministicEvidenceClassifier:
    """Evidence classifier backed by deterministic rules."""

    def classify(self, evidence: EvidenceItem) -> EvidenceClassification:
        content = evidence.content.lower()

        if any(
            indicator in content
            for indicator in HISTORICAL_LEGITIMATE_INDICATORS
        ):
            return EvidenceClassification.CONTRADICTING

        has_supporting_signal = any(
            indicator in content for indicator in SUPPORTING_INDICATORS
        )
        has_contradicting_signal = any(
            indicator in content for indicator in CONTRADICTING_INDICATORS
        )

        if has_supporting_signal and has_contradicting_signal:
            return EvidenceClassification.NEUTRAL

        if has_supporting_signal:
            return EvidenceClassification.SUPPORTING

        if has_contradicting_signal:
            return EvidenceClassification.CONTRADICTING

        return EvidenceClassification.NEUTRAL