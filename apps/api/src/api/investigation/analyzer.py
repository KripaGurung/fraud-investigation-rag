from api.investigation.schemas import AnalyzedEvidence, EvidenceClassification
from api.schemas.evidence import EvidenceBundle, EvidenceItem
from api.investigation.classifier import (
    DeterministicEvidenceClassifier,
    EvidenceClassifier,
)

def analyze_evidence(
    bundle: EvidenceBundle,
    classifier: EvidenceClassifier | None = None,
) -> list[AnalyzedEvidence]:
    """Analyze all evidence items in an evidence bundle."""
    if classifier is None:
        classifier = DeterministicEvidenceClassifier()   
    evidence_items = (
        bundle.transaction_evidence
        + bundle.historical_case_evidence
        + bundle.policy_evidence
    )

    analyzed_evidence = []

    for evidence in evidence_items:
        classification = classifier.classify(evidence)

        analyzed_evidence.append(
            AnalyzedEvidence(
                evidence=evidence,
                classification=classification,
                explanation=(
                    "Evidence classified as "
                    f"{classification.value}."
                ),
            )
        )

    return analyzed_evidence
