from api.investigation.context import InvestigationContext
from api.investigation.generation.schemas import InvestigationCase
from dataclasses import dataclass, field

@dataclass(frozen=True)
class CitationValidationResult:
    """Result of validating generated finding provenance."""

    invalid_evidence_ids: list[str] = field(default_factory=list)
    uncited_findings: list[str] = field(default_factory=list)

def validate_evidence_citations(
    case: InvestigationCase,
    context: InvestigationContext,
) -> list[str]:
    """Return generated evidence IDs that do not exist in the context."""
    valid_evidence_ids = {
        analyzed.evidence.source_id
        for analyzed in context.analyzed_evidence
    }

    cited_evidence_ids = {
        evidence_id
        for finding in (
            case.supporting_findings
            + case.contradicting_findings
        )
        for evidence_id in finding.evidence_ids
    }

    return sorted(cited_evidence_ids - valid_evidence_ids)


def validate_case_provenance(
    case: InvestigationCase,
    context: InvestigationContext,
) -> CitationValidationResult:
    """Validate evidence IDs and citation presence for generated findings."""
    invalid_evidence_ids = validate_evidence_citations(
        case,
        context,
    )

    findings = (
        case.supporting_findings
        + case.contradicting_findings
    )

    uncited_findings = [
        finding.statement
        for finding in findings
        if not finding.evidence_ids
    ]

    return CitationValidationResult(
        invalid_evidence_ids=invalid_evidence_ids,
        uncited_findings=uncited_findings,
    )