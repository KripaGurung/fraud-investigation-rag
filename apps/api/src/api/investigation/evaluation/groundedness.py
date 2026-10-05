from dataclasses import dataclass, field

from api.investigation.context import InvestigationContext
from api.investigation.generation.schemas import InvestigationCase

@dataclass(frozen=True)
class GroundednessResult:
    """Result of evaluating evidence grounding for generated findings."""

    score: float
    total_findings: int
    grounded_findings: int
    ungrounded_findings: list[str] = field(default_factory=list)

def _get_valid_evidence_ids(
    context: InvestigationContext,
) -> set[str]:
    """Return evidence IDs available in the investigation context."""
    return {
        analyzed.evidence.source_id
        for analyzed in context.analyzed_evidence
    }   

def _is_finding_grounded(
    evidence_ids: list[str],
    valid_evidence_ids: set[str],
) -> bool:
    """Return whether all citations for a finding reference available evidence."""
    if not evidence_ids:
        return False

    return all(
        evidence_id in valid_evidence_ids
        for evidence_id in evidence_ids
    ) 

def evaluate_groundedness(
    case: InvestigationCase,
    context: InvestigationContext,
) -> GroundednessResult:
    """Evaluate citation grounding across generated investigation findings."""
    valid_evidence_ids = _get_valid_evidence_ids(context)

    findings = (
        case.supporting_findings
        + case.contradicting_findings
    )

    grounded_findings = [
        finding
        for finding in findings
        if _is_finding_grounded(
            finding.evidence_ids,
            valid_evidence_ids,
        )
    ]

    ungrounded_findings = [
        finding.statement
        for finding in findings
        if not _is_finding_grounded(
            finding.evidence_ids,
            valid_evidence_ids,
        )
    ]

    total_findings = len(findings)
    grounded_count = len(grounded_findings)

    score = (
        grounded_count / total_findings
        if total_findings
        else 1.0
    )

    return GroundednessResult(
        score=score,
        total_findings=total_findings,
        grounded_findings=grounded_count,
        ungrounded_findings=ungrounded_findings,
    )