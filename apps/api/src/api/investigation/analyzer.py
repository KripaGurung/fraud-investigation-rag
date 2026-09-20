from api.investigation.schemas import AnalyzedEvidence, EvidenceClassification
from api.schemas.evidence import EvidenceBundle, EvidenceItem


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


def _classify_evidence(evidence: EvidenceItem) -> EvidenceClassification:
    """Classify one evidence item using deterministic keyword rules."""
    content = evidence.content.lower()

    if any(
        indicator in content for indicator in HISTORICAL_LEGITIMATE_INDICATORS
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

def analyze_evidence(bundle: EvidenceBundle) -> list[AnalyzedEvidence]:
    """Analyze all evidence items in an evidence bundle."""
    evidence_items = (
        bundle.transaction_evidence
        + bundle.historical_case_evidence
        + bundle.policy_evidence
    )

    analyzed_evidence = []

    for evidence in evidence_items:
        classification = _classify_evidence(evidence)

        analyzed_evidence.append(
            AnalyzedEvidence(
                evidence=evidence,
                classification=classification,
                explanation=(
                    "Deterministic classification based on evidence content: "
                    f"{classification.value}."
                ),
            )
        )

    return analyzed_evidence
