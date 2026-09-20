from dataclasses import dataclass

from api.investigation.analyzer import analyze_evidence
from api.investigation.gaps import detect_missing_evidence
from api.investigation.schemas import AnalyzedEvidence
from api.schemas.evidence import EvidenceBundle
from api.investigation.classifier import EvidenceClassifier


@dataclass(frozen=True)
class InvestigationContext:
    """Structured context used by the investigation pipeline."""

    analyzed_evidence: list[AnalyzedEvidence]
    missing_evidence: list[str]


def build_investigation_context(
    bundle: EvidenceBundle,
    classifier: EvidenceClassifier | None = None,
) -> InvestigationContext:
    """Build structured investigation context from an evidence bundle."""
    return InvestigationContext(
        analyzed_evidence=analyze_evidence(
            bundle,
            classifier=classifier,
        ),
        missing_evidence=detect_missing_evidence(bundle),
    )